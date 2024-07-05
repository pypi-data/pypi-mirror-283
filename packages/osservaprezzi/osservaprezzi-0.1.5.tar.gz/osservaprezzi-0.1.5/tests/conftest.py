"""Common fixtures for the Ecovacs tests."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any
from unittest.mock import AsyncMock, patch

from aiohttp import ClientError, ClientSession
import pytest

from osservaprezzi.client import Osservaprezzi

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator, Generator


@pytest.fixture
async def client() -> AsyncGenerator[Osservaprezzi, None]:
    async with ClientSession() as session:
        logging.basicConfig(level=logging.DEBUG)
        yield Osservaprezzi(session)


@pytest.fixture
def mock_client_get_response(
    response: dict[str, Any],
) -> Generator[dict[str, Any], None, None]:
    with patch("osservaprezzi.client.Osservaprezzi._get", return_value=response):
        yield response


@pytest.fixture
def mock_client_get_response_timeout() -> Generator[AsyncMock, None, None]:
    with patch(
        "aiohttp.ClientSession.get", side_effect=TimeoutError
    ) as mock_client_get_response_timeout:
        yield mock_client_get_response_timeout


@pytest.fixture
def mock_client_get_response_error() -> Generator[AsyncMock, None, None]:
    with patch(
        "aiohttp.ClientSession.get", side_effect=ClientError
    ) as mock_client_get_response_error:
        yield mock_client_get_response_error


@pytest.fixture
def mock_client_post_response(
    response: dict[str, Any],
) -> Generator[dict[str, Any], None, None]:
    with patch("osservaprezzi.client.Osservaprezzi._post", return_value=response):
        yield response


@pytest.fixture
def mock_client_post_response_timeout() -> Generator[AsyncMock, None, None]:
    with patch(
        "aiohttp.ClientSession.post", side_effect=TimeoutError
    ) as mock_client_get_response_timeout:
        yield mock_client_get_response_timeout


@pytest.fixture
def mock_client_post_response_error() -> Generator[AsyncMock, None, None]:
    with patch(
        "aiohttp.ClientSession.post", side_effect=ClientError
    ) as mock_client_post_response_error:
        yield mock_client_post_response_error
