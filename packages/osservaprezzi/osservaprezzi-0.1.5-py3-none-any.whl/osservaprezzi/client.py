"""Osservaprezzi module."""

from __future__ import annotations

from http import HTTPStatus
import logging
from typing import TYPE_CHECKING, Any

from aiohttp import ClientError, ClientSession

from osservaprezzi.helpers import (
    brand_from_json,
    fuel_from_json,
    station_from_json,
)

from .const import (
    DEFAULT_TIMEOUT,
    PATH_API_BRANDS,
    PATH_API_FUELS,
    PATH_API_SERVICE_AREA,
    PATH_API_ZONES,
    REQUEST_HEADERS,
    URL_API_ENDPOINT,
)
from .exceptions import ApiError, ApiTimeoutError

if TYPE_CHECKING:
    from .models import Brand, Fuel, GPSCoordinates, Station

_LOGGER = logging.getLogger(__name__)


class Osservaprezzi:
    """Osservaprezzi client class."""

    def __init__(self, session: ClientSession) -> None:
        self._session = session

    async def get_brands(self) -> list[Brand]:
        """Get brands."""
        json = await self._get(PATH_API_BRANDS)
        return [brand_from_json(data) for data in json.get("loghi", [])]

    async def get_fuels(self) -> list[Fuel]:
        """Get registered fuels."""
        json = await self._get(PATH_API_FUELS)
        return [fuel_from_json(data) for data in json.get("results", [])]

    async def get_stations(
        self,
        coordinates: GPSCoordinates,
        *,
        radius: int = 5,
        fuel_type: str | None = None,
    ) -> list[Station]:
        """Get stations."""
        payload = {"points": [coordinates.to_json()], "radius": radius}
        if fuel_type is not None:
            payload["fuelType"] = fuel_type
        json = await self._post(PATH_API_ZONES, payload)
        return [station_from_json(data) for data in json.get("results", [])]

    async def get_station(self, station_id: int) -> Station | None:
        """Get station."""
        json = await self._get(PATH_API_SERVICE_AREA % station_id)
        return station_from_json(json) if "id" in json else None

    async def _get(self, path: str) -> dict[str, Any]:
        """Perform a GET request."""
        try:
            url = f"{URL_API_ENDPOINT}/{path}"
            async with self._session.get(
                url, timeout=DEFAULT_TIMEOUT, headers=REQUEST_HEADERS
            ) as response:
                if response.status == HTTPStatus.OK:
                    response_data: dict[str, Any] = await response.json()
                    return response_data
        except TimeoutError as ex:
            raise ApiTimeoutError from ex
        except ClientError as ex:
            raise ApiError from ex

        raise ApiError("Unknown error occurred")

    async def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        """Perform a POST request."""
        try:
            url = f"{URL_API_ENDPOINT}/{path}"
            async with self._session.post(
                url,
                json=payload,
                timeout=DEFAULT_TIMEOUT,
                headers=REQUEST_HEADERS,
            ) as response:
                if response.status == HTTPStatus.OK:
                    response_data: dict[str, Any] = await response.json()
                    return response_data
        except TimeoutError as ex:
            raise ApiTimeoutError from ex
        except ClientError as ex:
            raise ApiError from ex

        raise ApiError("Unknown error occurred")
