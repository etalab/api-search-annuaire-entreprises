import os
from datetime import timedelta

from aio_proxy.decorators.http_exception import http_exception_handler
from aio_proxy.exceptions.siren import InvalidSirenError
from aio_proxy.response.formatters.convention_collective import (
    extract_list_idcc_by_siren_from_ul,
)
from aio_proxy.search.parsers.siren import is_siren
from aio_proxy.search.queries.search_by_siren import search_by_siren
from aio_proxy.utils.cache import cache_strategy
from aio_proxy.utils.helpers import fetch_json_from_url
from aiohttp import web

TIME_TO_LIVE = timedelta(days=1)
URL_CC_JSON = os.getenv("METADATA_URL_CC_JSON")


def should_cache_search_response():
    return True


def get_metadata_json():
    return fetch_json_from_url(URL_CC_JSON)


@http_exception_handler
def get_metadata_cc_response():
    cache_key = "cc_kali_json"
    json_content = cache_strategy(
        cache_key,
        get_metadata_json,
        should_cache_search_response,
        TIME_TO_LIVE,
    )
    return web.json_response(json_content)


@http_exception_handler
def get_cc_list_by_siren(request):
    """
    Retrieves the list of IDCCs associated with a given SIREN number.

    Args:
        request (aiohttp.web.Request): The HTTP request object containing 'siren'
        in match_info.

    Returns:
        aiohttp.web.Response: JSON response containing the list of IDCCs or an empty
        list if no match found.

    Raises:
        ValueError: If the SIREN number is invalid.
    """
    siren = request.match_info["siren"]
    if not is_siren(siren):
        raise InvalidSirenError()
    match_siren = search_by_siren(siren)

    if not match_siren:
        return web.json_response([])

    list_idcc = extract_list_idcc_by_siren_from_ul(match_siren)
    return web.json_response(list_idcc)
