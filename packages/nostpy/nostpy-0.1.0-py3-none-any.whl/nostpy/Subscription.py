import asyncio
import json
from typing import List, Tuple, Dict
from fastapi.responses import JSONResponse
import secp256k1

class Subscription:
    """
    Represents a subscription object with attributes and methods for handling subscription-related operations.

    Attributes:
        filters (dict): Dictionary containing filters for the subscription.
        subscription_id (str): The ID of the subscription.
        where_clause (str): The WHERE clause of the base SQL query.
        base_query (str): The base SQL query for fetching events.
        column_names (List): List of column names for event attributes.

    Methods:
        generate_tag_clause: Generates the tag clause for SQL query based on given tags.
        sanitize_event_keys: Sanitizes the event keys by mapping and filtering the filters.
        parse_sanitized_keys: Parses and sanitizes the updated keys to generate tag values and query parts.
        generate_query: Generates the SQL query based on provided tags.
        _parser_worker: Worker function to parse and add records to the column.
        query_result_parser: Parses the query result and adds columns accordingly.
        fetch_data_from_cache: Fetches data from cache based on the provided Redis key.
        parse_filters: Parses and sanitizes filters to generate tag values and query parts.
        sub_response_builder: Builds and returns the JSON response for the subscription.
    """

    def __init__(self, request_payload: dict) -> None:
        self.filters = request_payload.get("event_dict", {})
        self.subscription_id = request_payload.get("subscription_id")
        self.where_clause = ""
        self.column_names = [
            "id",
            "pubkey",
            "kind",
            "created_at",
            "tags",
            "content",
            "sig",
        ]

    def _generate_tag_clause(self, tags) -> str:
        tag_clause = (
            " EXISTS ( SELECT 1 FROM jsonb_array_elements(tags) as elem WHERE {})"
        )
        conditions = [f"elem @> '{tag_pair}'" for tag_pair in tags]

        complete_cluase = tag_clause.format(" OR ".join(conditions))
        return complete_cluase

    def _search_clause(self, search_item):
        search_clause = f" EXISTS ( SELECT 1 FROM jsonb_array_elements(tags) as elem WHERE elem::text LIKE '%{search_item}%' OR content LIKE '%{search_item}%')"
        return search_clause

    async def _sanitize_event_keys(self, filters, logger) -> Dict:
        updated_keys = {}
        limit = ""
        global_search = {}
        try:
            try:
                limit = filters.get("limit", 100)
                filters.pop("limit")
            except Exception as exc:
                logger.error(f"Exception is: {exc}")

            try:
                global_search = filters.get("search", {})
                filters.pop("search")
            except Exception as exc:
                logger.error(f"Exception is: {exc}")

            key_mappings = {
                "authors": "pubkey",
                "kinds": "kind",
                "ids": "id",
            }

            if filters:
                for key in filters:
                    new_key = key_mappings.get(key, key)
                    if new_key != key:
                        stored_val = filters[key]
                        updated_keys[new_key] = stored_val
                    else:
                        updated_keys[key] = filters[key]

            return updated_keys, limit, global_search
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}", exc_info=True)
            return updated_keys, limit, global_search

    async def _parse_sanitized_keys(self, updated_keys, logger) -> Tuple[List, List]:
        query_parts = []
        tag_values = []

        try:
            for item in updated_keys:
                outer_break = False

                if item.startswith("#"):
                    try:
                        for tags in updated_keys[item]:
                            tag_values.append(json.dumps([item[1], tags]))

                        outer_break = True
                        continue
                    except TypeError as e:
                        logger.error(f"Error processing tags for key {item}: {e}")

                elif item in ["since", "until"]:
                    if item == "since":
                        since = f'created_at > {updated_keys["since"]}'
                        query_parts.append(since)
                        outer_break = True
                        continue
                    elif item == "until":
                        until = f'created_at < {updated_keys["until"]}'
                        query_parts.append(until)
                        outer_break = True
                        continue

                if outer_break:
                    continue

                array_search = f"{item} = ANY(ARRAY {updated_keys[item]})"
                query_parts.append(array_search)

            return tag_values, query_parts
        except Exception as exc:
            logger.warning(
                f"query not sanitized (maybe empty value) tv is {tag_values}, qp is {query_parts}, error is: {exc}",
                exc_info=True,
            )
            return tag_values, query_parts

    async def _parser_worker(self, record, column_added) -> None:
        row_result = {}
        i = 0
        for item in record:
            row_result[self.column_names[i]] = item
            i += 1
        column_added.append([row_result])

    async def query_result_parser(self, query_result) -> List:
        column_added = []
        try:
            tasks = [
                self._parser_worker(record, column_added) for record in query_result
            ]
            await asyncio.gather(*tasks)
            return column_added
        except:
            return None

    def fetch_data_from_cache(self, redis_key, redis_client) -> bytes:
        cached_data = redis_client.get(redis_key)
        if cached_data:
            return cached_data
        else:
            return None

    async def parse_filters(self, filters: dict, logger) -> tuple:
        updated_keys, limit, global_search = await self._sanitize_event_keys(
            filters, logger
        )
        logger.debug(f"Updated keys is: {updated_keys}")
        if updated_keys:
            tag_values, query_parts = await self._parse_sanitized_keys(
                updated_keys, logger
            )
            return tag_values, query_parts, limit, global_search
        else:
            return {}, {}, None, {}

    def base_query_builder(self, tag_values, query_parts, limit, global_search, logger):
        try:
            if query_parts:
                self.where_clause = " AND ".join(query_parts)

            if tag_values:
                tag_clause = self._generate_tag_clause(tag_values)
                self.where_clause += f" AND {tag_clause}"

            if global_search:
                search_clause = self._search_clause(global_search)
                self.where_clause += f" AND {search_clause}"

            if not limit or limit > 100:
                limit = 100

            self.base_query = f"SELECT * FROM events WHERE {self.where_clause} ORDER BY created_at DESC LIMIT {limit} ;"
            logger.debug(f"SQL query constructed: {self.base_query}")
            return self.base_query
        except Exception as exc:
            logger.error(f"Error building query: {exc}", exc_info=True)
            return None

    def sub_response_builder(
        self, event_type, subscription_id, results_json, http_status_code
    ):
        return JSONResponse(
            content={
                "event": event_type,
                "subscription_id": subscription_id,
                "results_json": results_json,
            },
            status_code=http_status_code,
        )