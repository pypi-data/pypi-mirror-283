from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from osservaprezzi.exceptions import ApiError, ApiTimeoutError
from osservaprezzi.models import GPSCoordinates

if TYPE_CHECKING:
    from osservaprezzi.client import Osservaprezzi


@pytest.mark.usefixtures("client", "mock_client_get_response_timeout")
async def test_get_response_timeout(
    client: Osservaprezzi,
) -> None:
    with pytest.raises(ApiTimeoutError):
        await client.get_fuels()


@pytest.mark.usefixtures("client", "mock_client_get_response_error")
async def test_get_response_error(
    client: Osservaprezzi,
) -> None:
    with pytest.raises(ApiError):
        await client.get_fuels()


@pytest.mark.usefixtures("client", "mock_client_post_response_timeout")
async def test_post_response_timeout(
    client: Osservaprezzi,
) -> None:
    with pytest.raises(ApiTimeoutError):
        await client.get_stations(GPSCoordinates(45.542662, 10.225224), radius=5)


@pytest.mark.usefixtures("client", "mock_client_post_response_error")
async def test_post_response_error(
    client: Osservaprezzi,
) -> None:
    with pytest.raises(ApiError):
        await client.get_stations(GPSCoordinates(45.542662, 10.225224), radius=5)
