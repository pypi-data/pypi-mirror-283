from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest

from osservaprezzi.helpers import (
    brand_from_json,
    fuel_from_json,
    gps_coordinates_from_json,
    marker_from_json,
    service_from_json,
    station_from_json,
)

if TYPE_CHECKING:
    from syrupy.assertion import SnapshotAssertion


@pytest.mark.parametrize(
    "json",
    [
        {"bandieraId": 1, "bandiera": "Brand #1"},
        {
            "bandieraId": 2,
            "bandiera": "Brand #2",
            "logoMarkerList": [
                {
                    "tipoFile": "logo",
                    "estensione": "png",
                    "content": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==",
                }
            ],
        },
    ],
)
async def test_brand_from_json(
    snapshot: SnapshotAssertion,
    json: dict[str, Any],
) -> None:
    assert snapshot(name="brand_from_json") == brand_from_json(json)


@pytest.mark.parametrize(
    "json",
    [
        {"id": "1-x", "description": "Benzina"},
        {
            "id": 75557219,
            "price": 2.079,
            "name": "Benzina",
            "fuelId": 1,
            "isSelf": False,
        },
        {
            "id": 75557219,
            "price": 2.079,
            "name": "Benzina",
            "fuelId": 1,
            "isSelf": False,
            "insertDate": "2024-07-02T12:00:38Z",
            "validityDate": "2024-07-02T11:59:00Z",
        },
    ],
)
async def test_fuel_from_json(
    snapshot: SnapshotAssertion,
    json: dict[str, Any],
) -> None:
    assert snapshot(name="fuel_from_json") == fuel_from_json(json)


@pytest.mark.parametrize(
    "json",
    [{"lat": 0, "lng": 0}, {"lat": 45.541553, "lng": 10.211802}],
)
async def test_gps_coordinates_from_json(
    snapshot: SnapshotAssertion,
    json: dict[str, Any],
) -> None:
    assert snapshot(name="gps_coordinates_from_json") == gps_coordinates_from_json(json)


@pytest.mark.parametrize(
    "json",
    [
        {
            "tipoFile": "logo",
            "estensione": "png",
            "content": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==",
        }
    ],
)
async def test_marker_from_json(
    snapshot: SnapshotAssertion,
    json: dict[str, Any],
) -> None:
    assert snapshot(name="marker_from_json") == marker_from_json(json)


@pytest.mark.parametrize(
    "json",
    [{"id": 1, "description": "Dummy Service"}, {"id": 6, "description": "Bancomat"}],
)
async def test_service_from_json(
    snapshot: SnapshotAssertion,
    json: dict[str, Any],
) -> None:
    assert snapshot(name="service_from_json") == service_from_json(json)


@pytest.mark.parametrize(
    "json",
    [
        {
            "id": 1,
            "name": "Service Area 1",
            "fuels": [
                {
                    "id": 10001,
                    "price": 2.079,
                    "name": "Benzina",
                    "fuelId": 1,
                    "isSelf": False,
                },
                {
                    "id": 10002,
                    "price": 1.869,
                    "name": "Benzina",
                    "fuelId": 1,
                    "isSelf": True,
                },
                {
                    "id": 10003,
                    "price": 1.989,
                    "name": "Gasolio",
                    "fuelId": 2,
                    "isSelf": False,
                },
                {
                    "id": 10004,
                    "price": 1.779,
                    "name": "Gasolio",
                    "fuelId": 2,
                    "isSelf": True,
                },
            ],
            "location": {
                "lat": 1.5,
                "lng": 5.9,
            },
            "insertDate": "1985-05-01T18:20:00+01:00",
            "address": "This is the service area address",
            "brand": "Octan",
        },
        {
            "id": 2,
            "name": "Service Area 2",
            "fuels": [
                {
                    "id": 20001,
                    "price": 1.839,
                    "name": "Benzina",
                    "fuelId": 1,
                    "isSelf": True,
                },
                {
                    "id": 20002,
                    "price": 1.709,
                    "name": "Gasolio",
                    "fuelId": 2,
                    "isSelf": True,
                },
            ],
            "location": {"lat": 1.6, "lng": 4.7},
            "insertDate": "1985-09-05T11:56:40+01:00",
            "brand": "Octan",
        },
        {
            "id": 1,
            "name": "Octan Service Area",
            "nomeImpianto": "Octan Service Area",
            "address": "Service Area Address",
            "brand": "Octan",
            "fuels": [
                {
                    "id": 20001,
                    "price": 1.839,
                    "name": "Benzina",
                    "fuelId": 1,
                    "isSelf": True,
                    "serviceAreaId": 1,
                    "insertDate": "2024-07-02T12:00:38Z",
                    "validityDate": "2024-07-02T11:59:00Z",
                },
                {
                    "id": 20002,
                    "price": 1.709,
                    "name": "Gasolio",
                    "fuelId": 2,
                    "isSelf": True,
                    "serviceAreaId": 1,
                    "insertDate": "2024-07-02T12:00:38Z",
                    "validityDate": "2024-07-02T11:59:00Z",
                },
            ],
            "phoneNumber": "",
            "email": "",
            "website": "",
            "company": "Ugo Legozzi",
            "services": [{"id": 6, "description": "Bancomat"}],
        },
    ],
)
async def test_station_from_json(
    snapshot: SnapshotAssertion,
    json: dict[str, Any],
) -> None:
    assert snapshot(name="station_from_json") == station_from_json(json)
