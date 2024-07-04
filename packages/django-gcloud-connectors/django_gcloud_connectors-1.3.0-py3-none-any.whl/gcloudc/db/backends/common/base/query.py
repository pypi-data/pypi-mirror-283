import math
import warnings
from typing import List, Set, Union

from .entity import Key, Entity
from .connection import Wrapper
from gcloudc.db.backends.common.helpers import entity_matches_query
from django.db import ProgrammingError
from functools import cmp_to_key

#  This is a list of the possible operators accepted by the query class when adding
#  filters. It may seem that there should be more of these (e.g. IN, contains-any etc.)
#  However:
#    - Even on Firestore, OR queries are performed on disjunctive normal form representations
#      of the query, that's exactly what we're doing anyway so using the Firestore version
#      probably doesn't buy us much, at the cost of increased complexity
#    - contains-any is just the same thing, it goes through the list of values running an OR
#      query
#    - contains is just an equality on a list property, it's a little counter intuitive but that's
#      what it is
#    - is null is just `= None`


class Operator:
    EQ = "="
    LT = "<"
    LTE = "<="
    GT = ">"
    GTE = ">="


class Query:
    def __init__(
        self, wrapper: Wrapper, table_or_path,
        only_return_keys=False,
        only_return_fields=None,
        namespace=None,
        is_nested_collection=False,  # Whether this query is for a nested collection or not
    ):
        wrapper.ensure_connection()

        self.connection = wrapper.connection
        self.wrapper = wrapper
        self.namespace = namespace
        self.only_return_keys = only_return_keys
        self.only_return_fields = only_return_fields or []
        self.path = (
            table_or_path
            if isinstance(table_or_path, (list, tuple))
            else [table_or_path]
        )

        # A dict of (col, op): [values] of filters
        # that have been added to this query
        self._filters = {}

        # A list of orderings that have been added to this query
        self._orderings = []

    @property
    def filters(self):
        return self._filters

    def distinct_on(self, fields):
        raise NotImplementedError()

    def has_filter(self, property, operator) -> bool:
        return (property, operator) in self._filters

    def get_filter(self, property, operator):
        return self._filters.get((property, operator))

    def _add_filter(self, property, operator, value):
        raise NotImplementedError()

    def add_filter(self, property, operator, value):
        self._add_filter(property, operator, value)
        self._filters.setdefault((property, operator), []).append(value)

    def fetch(self, offset, limit):
        raise NotImplementedError()

    def count(self, limit):
        raise NotImplementedError()

    def order_by(self, orderings):
        self._order_by(orderings)
        self._orderings.extend(orderings)

    def _order_by(self, orderings):
        raise NotImplementedError()

    def __repr__(self):
        return f"<Query {self.filters!r}>"


class ChunkedResultset(object):
    def __init__(self, query, limit, chunk_size=50):
        self.query = query
        self.limit = limit
        self.chunk_size = (
            min(limit, chunk_size)
            if limit is not None
            else chunk_size
        )

        self.fetched = self._fetch()

    def _fetch(self):
        total = self.limit or math.inf

        offset = 0
        limit = self.chunk_size
        while offset < total:
            yielded = 0
            for entity in self.query.fetch(offset=offset, limit=limit):
                assert (entity is not None)
                yield entity
                yielded += 1

            if not yielded:
                break

            offset += self.chunk_size

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.fetched)


def _query_has_inequality(query):
    inequality_ops = frozenset([">", "<", "<=", ">="])

    for _, op in query.filters:
        if op in inequality_ops:
            return True
    return False


class ORQuery:

    def __init__(
            self, wrapper: Wrapper, table_or_path, unique_combinations,
            only_return_keys=False, only_return_fields=None,
            namespace=None, select=None, distinct_fields=None,
            annotations=None
        ):  # noqa

        self.wrapper = wrapper
        self.queries: List[Query] = []

        # self.select is the list of properties that an entity should have when
        # it is returned. This is used externally to know what must be returned to Django
        # when the results are processed. It's not always the same as only_return_fields
        # and is set by the query parsing process
        self.select = select

        self.unique_combinations = unique_combinations
        self.only_return_keys = only_return_keys
        self.only_return_fields = only_return_fields or []
        self.distinct_fields = distinct_fields
        self.path = (
            table_or_path
            if isinstance(table_or_path, (list, tuple))
            else [table_or_path]
        )
        self.ordering = []
        self.namespace = namespace
        self._excluded_keys: Set[Key] = set()

        # Annotations are in the form of (column, transform func, arguments)
        # and are used to add additional data to entities being returned from
        # queries
        self.annotations = annotations or []

    def set_excluded_keys(self, keys: Set[Key]):
        self._excluded_keys = keys

    def push_query(self, connection) -> Query:
        query_class = connection.get_query_class()
        query = query_class(
            connection,
            self.path,
            only_return_keys=self.only_return_keys,
            only_return_fields=self.only_return_fields,
            namespace=self.namespace
        )
        self.queries.append(query)
        return query

    def query_count(self) -> int:
        return len(self.queries)

    def query_at(self, i) -> Query:
        return self.queries[i]

    def order_by(self, ordering):
        self.ordering = ordering

    def _apply_ordering(self):
        for query in self.queries:
            query.order_by(self.ordering)

    def _apply_distinct(self):
        if self.distinct_fields is None:
            return

        for query in self.queries:
            query.distinct_on(self.distinct_fields)

    def _can_use_get(self) -> bool:
        """
            Returns true if every subquery does an equality filter on a key
        """

        for query in self.queries:
            if not query.has_filter(self.wrapper.key_property_name(), Operator.EQ):
                return False
        else:
            return True

    def _unique_combo_for_query(self, query):
        """
            If this query has filters on a unique combination
            this returns that combination of fields, otherwise
            returns None
        """

        for combo in self.unique_combinations:
            found = 0
            for field in combo:
                if query.has_filter(field, "="):
                    found += 1
                    continue

            if found == len(combo):
                return combo

        return None

    def _extract_keys(self) -> List[Key]:
        assert (self._can_use_get())
        result = []
        for query in self.queries:
            value = query.get_filter(self.wrapper.key_property_name(), Operator.EQ)
            if len(value) > 1:
                # If we have a key equality on more than one value
                # it won't return anything, so do nothing
                continue

            result.append(value[0])

        return result

    def _check_queries_dont_match_cached_entities(self):
        """
            If we have an item in the transaction cache, and you make a query
            for something that could match that cache we raise an exception to protect
            you from accessing stale results. Items only go into the cache when you put
            them, so if you subsequently run a query that would match a previously put
            item you won't get it back.
        """

        for query in self.queries:
            query.wrapper.ensure_connection()
            for v in query.wrapper.connection._cache.values():
                if entity_matches_query(v, query):
                    raise ProgrammingError(
                        f"Performed query on collection {query.path} in a transaction "
                        "that would match a document which has already been put"
                    )

    def _apply_annotations(self, entity):
        for col, func, args in self.annotations:
            entity[col] = func(entity, *args)

    def _should_use_get(self):
        if not self._can_use_get():
            return False

        # If we have more than one query, and we can
        # use get, then we should always use get
        if len(self.queries) > 1:
            return True

        # If we have one key-filter query, and it contains
        # an inequality - then we should use a get to avoid
        # having to create additional indexes
        if _query_has_inequality(self.queries[0]):
            return True

        # Finally, if we are projecting, or doing a keys_only
        # query, we should avoid using get
        if self.queries[0].only_return_fields or self.queries[0].only_return_keys:
            return False

        return True

    def fetch(self, offset, limit):

        def cmp(a, b) -> int:
            if a.less_than(b, self.ordering, self.wrapper.key_property_name()):
                return -1
            elif b.less_than(a, self.ordering, self.wrapper.key_property_name()):
                return 1
            return 0

        # FIXME: deduplicate distinct entities

        # FIXME: Make async
        self._apply_ordering()
        self._apply_distinct()

        original_limit = limit

        # If we are excluding keys from the resultset, then
        # we need to fetch more results than requested
        if self._excluded_keys and limit is not None:
            limit += len(self._excluded_keys)

        resultsets = []
        if self._should_use_get():
            # Optimisation, if we can do a get() query with the available
            # keys then do that because multiple key filters will mean many
            # queries, when we can just do one and then filter in memory
            keys = self._extract_keys()
            wrapper = self.queries[0].wrapper
            conn = wrapper.connection
            max_keys_per_get = 1000
            resultsets = []

            to_fetch, remaining = keys[:max_keys_per_get], keys[max_keys_per_get:]
            while to_fetch or remaining:
                resultsets.extend(conn.get([x for x in to_fetch if x]))
                to_fetch, remaining = remaining[:max_keys_per_get], remaining[max_keys_per_get:]

            resultsets = [
                iter([x]) for x in resultsets
                if any([entity_matches_query(x, qry) for qry in self.queries])
            ]
        elif len(self.queries) == 1:
            # Simple case, single query branch (no OR) so we can leverage
            # the database directly for most things
            qry = self.queries[0]

            # Optimisation, if we're filtering on a single key
            # and that key is in the cache, then fallback to
            # that. If the key isn't in the cache it's still more
            # optimal to do a query than a get()
            cache_hit = False
            combo = self._unique_combo_for_query(qry)

            if self._can_use_get():
                keys = self._extract_keys()
                if keys and keys[0] in qry.connection._cache:
                    # Set the resultsets and fall through
                    cache_hit = True
                    resultsets = [
                        [qry.connection.get(keys[0])]
                    ]

                    resultsets[0].sort(key=cmp_to_key(cmp))
                    resultsets[0] = iter(resultsets[0])
            elif combo:
                # Unique combination optimisation. If we query on a unique
                # combination, and that exists in the cache, then don't do
                # a query
                values = [(k, qry.get_filter(k, "=")[0]) for k in combo]
                entity = qry.connection._find_entity_in_cache(values)
                if entity:
                    cache_hit = True
                    resultsets = [iter([entity])]

            if not cache_hit:
                self._check_queries_dont_match_cached_entities()

                returned_count = 0
                for entity in qry.fetch(offset=offset, limit=limit):
                    if limit is not None and returned_count == original_limit:
                        return

                    key = entity.key()
                    if key in self._excluded_keys:
                        continue

                    self._apply_annotations(entity)
                    returned_count += 1
                    yield entity
        else:
            # FIXME: Should we handle looking up unique entities in the cache
            # in multi-query situations? We currently only do this in the single-query
            # version
            self._check_queries_dont_match_cached_entities()

            # We have to overfetch if we're doing multiple
            # queries
            if limit is not None:
                offset = offset or 0
                limit = offset + limit

            # IN queries can become very memory intensive so we
            # cap the number we fetch in one go. We try to fetch
            # a number per query, but don't go past
            # max_entities_in_memory / query_count
            entities_per_chunk = 1000
            max_entities_in_memory = 5000
            chunk_size = min(
                max_entities_in_memory // len(self.queries),
                entities_per_chunk * len(self.queries)
            )

            for qry in self.queries:
                resultsets.append(
                    ChunkedResultset(
                        qry,
                        limit=limit,
                        chunk_size=chunk_size
                    )
                )

        # Go through each outstanding result queue and store
        # the next entry of each (None if the result queue is done)
        next_entries = [None] * len(resultsets)

        def shift_queue(idx):
            while True:
                try:
                    next_entries[idx] = next(resultsets[idx])
                except StopIteration:
                    next_entries[idx] = None
                    break
                else:
                    key = next_entries[idx].key()
                    if key in self._excluded_keys:
                        continue
                    else:
                        break

        for i in range(len(resultsets)):
            shift_queue(i)

        returned_count = 0
        yielded_count = 0

        seen_keys = set()  # For de-duping results
        while any([x for x in next_entries if x is not None]):

            def get_next():
                idx, lowest = None, None

                for i, entry in enumerate(next_entries):
                    if entry is None:
                        continue

                    if lowest is None or self._less_than(entry, lowest, self.ordering):
                        idx, lowest = i, entry

                # Move the queue along if we found the entry there
                if lowest is not None and idx is not None:
                    shift_queue(idx)

                return lowest

            # Find the next entry from the available queues
            next_entity = get_next()

            # No more entries if this is the case
            if next_entity is None:
                break

            next_key = next_entity.key()

            # Make sure we haven't seen this result before before yielding
            if next_key not in seen_keys:
                returned_count += 1
                seen_keys.add(next_key)

                if offset and returned_count <= offset:
                    # We haven't hit the offset yet, so just
                    # keep fetching entities
                    continue

                self._apply_annotations(next_entity)

                yielded_count += 1
                yield next_entity

                if limit and yielded_count == original_limit:
                    break

    def count(self, limit=None):
        # FIXME: deduplicate distinct entities
        original_limit = limit

        results = []
        if self._excluded_keys:
            if self.wrapper._count_mode == "native":
                # TODO: This potentially can be fixed by using:
                #  query.add_filter(self.wrapper.key_property_name(), "NOT_IN", self._excluded_keys)
                #  however SDK doesn't like __key__ filters with "NOT_IN"
                #  even though DataStore does support this

                warnings.warn("Count queries with exclude are emulated even in native mode")
            if limit is not None:
                limit += len(self._excluded_keys)

            # We have to skip these manually
            for query in self.queries:
                query.only_return_keys = True
                count = 0
                for result in query.fetch(offset=None, limit=limit):
                    if result.key() in self._excluded_keys:
                        continue
                    else:
                        count += 1
                results.append(count)
        else:
            for query in self.queries:
                results.append(query.count(limit=limit))

        result = sum(results)
        if original_limit is not None:
            return min(result, original_limit)
        else:
            return result

    def _less_than(self, lhs: Union[Entity, Key], rhs: Union[Entity, Key], ordering: List[str]) -> bool:
        """
            Returns True if lhs < rhs depending on the ordering.
        """

        if isinstance(lhs, Key) and isinstance(rhs, Key):
            return lhs < rhs
        elif isinstance(lhs, Key) != isinstance(rhs, Key):
            raise ValueError("Tried to compare Entity with Key")

        # Handle None cases (None is always less)
        if lhs is None and rhs is None:
            return False
        elif lhs is None:
            return True
        elif rhs is None:
            return False

        return lhs.less_than(
            rhs, ordering,
            self.queries[0].wrapper.key_property_name()
        )

    def __repr__(self):
        queries_repr = "\n".join([f'\t{x!r}' for x in self.queries])
        return f"<ORQuery \n{queries_repr}\n>"
