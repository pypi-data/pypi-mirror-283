from __future__ import annotations

from typing import TYPE_CHECKING

from attr import dataclass
import pytest

from osservaprezzi.models import GPSCoordinates

if TYPE_CHECKING:
    from syrupy.assertion import SnapshotAssertion

    from osservaprezzi.client import Osservaprezzi


@dataclass
class StationsTest:
    """Stations test class."""

    location: GPSCoordinates
    radius: int


@pytest.mark.usefixtures("client", "mock_client_post_response")
@pytest.mark.parametrize(
    ("test", "response"),
    [
        (
            StationsTest(location=GPSCoordinates(45.542662, 10.225224), radius=5),
            {
                "success": True,
                "center": {"lat": 1.745, "lng": 5.934},
                "results": [
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
                ],
            },
        ),
        (
            StationsTest(location=GPSCoordinates(0.0, 0.0), radius=1),
            {
                "success": True,
                "center": {"lat": 0.0, "lng": 0.0},
                "results": [],
            },
        ),
    ],
)
async def test_stations(
    client: Osservaprezzi,
    snapshot: SnapshotAssertion,
    test: StationsTest,
) -> None:
    assert snapshot(name="stations") == await client.get_stations(
        test.location, radius=test.radius
    )


@pytest.mark.usefixtures("client", "mock_client_get_response")
@pytest.mark.parametrize(
    ("station_id", "response"),
    [
        (
            1,
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
        ),
    ],
)
async def test_single_station(
    client: Osservaprezzi,
    snapshot: SnapshotAssertion,
    station_id: int,
) -> None:
    assert snapshot(name=f"station_{station_id}") == await client.get_station(
        station_id
    )
