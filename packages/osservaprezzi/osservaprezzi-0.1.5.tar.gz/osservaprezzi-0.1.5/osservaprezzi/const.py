"""Constants module."""

from __future__ import annotations

DEFAULT_TIMEOUT = 10
URL_API_ENDPOINT = "https://carburanti.mise.gov.it/ospzApi"
PATH_API_BRANDS = "registry/alllogos"
PATH_API_FUELS = "registry/fuels"
PATH_API_ZONES = "search/zone"
PATH_API_SERVICE_AREA = "registry/servicearea/%d"
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Origin": "https://carburanti.mise.gov.it",
    "Host": "carburanti.mise.gov.it",
}
