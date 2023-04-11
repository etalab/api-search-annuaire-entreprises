import json
import logging
from collections.abc import Callable

from aio_proxy.decorators.http_exception import http_exception_handler
from aio_proxy.response.format_response import format_response
from aio_proxy.response.format_search_results import format_search_results
from aio_proxy.search.index import ElasticsearchSireneIndex
from aiohttp import web
from sentry_sdk import capture_exception, push_scope


@http_exception_handler
def api_response(
    request, extract_function: Callable, search_function: Callable
) -> dict[str, int]:
    """Create and format API response.

    Args:
        request: HTTP request.
        extract_function (Callable): function used to extract parameters.
        search_function (Callable): function used for search .
    Returns:
        response in json format (results, total_results, page, per_page,
        total_pages)
    """
    try:
        parameters, page, per_page = extract_function(request)
        search_results = search_function(
            ElasticsearchSireneIndex, page * per_page, per_page, **parameters
        )
        total_results = search_results["total_results"]
        results = search_results["response"]
        execution_time = search_results["execution_time"]
        include_etablissements = search_results["include_etablissements"]
        include_slug = search_results["include_slug"]
        results_formatted = format_search_results(
            results, include_etablissements, include_slug
        )
        response_formatted = format_response(
            results_formatted, total_results, page, per_page, execution_time
        )
        return web.json_response(text=json.dumps(response_formatted, default=str))
    except ValueError as error:
        with push_scope() as scope:
            # group value errors together based on their response (Bad request)
            scope.fingerprint = ["Bad Request"]
            # capture_exception(error)
            logging.warning(f"Bad request: {error}")
            raise error
    # capture error in Sentry
    except Exception as error:
        # capturing error at this level allows us to get the actual error before it's
        # wrapped in http_exception_handler
        capture_exception(error)
        raise error
