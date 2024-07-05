from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from syrupy.assertion import SnapshotAssertion

    from osservaprezzi.client import Osservaprezzi


@pytest.mark.usefixtures("client", "mock_client_get_response")
@pytest.mark.parametrize(
    "response",
    [
        {
            "results": [
                {"id": "1-x", "description": "Benzina"},
                {"id": "1-1", "description": "Benzina (Self)"},
                {"id": "1-0", "description": "Benzina (Servito)"},
                {"id": "2-x", "description": "Gasolio"},
                {"id": "2-1", "description": "Gasolio (Self)"},
                {"id": "2-0", "description": "Gasolio (Servito)"},
                {"id": "3-x", "description": "Metano"},
                {"id": "3-1", "description": "Metano (Self)"},
                {"id": "3-0", "description": "Metano (Servito)"},
                {"id": "4-x", "description": "GPL"},
                {"id": "4-1", "description": "GPL (Self)"},
                {"id": "4-0", "description": "GPL (Servito)"},
                {"id": "323-x", "description": "L-GNC"},
                {"id": "323-1", "description": "L-GNC (Self)"},
                {"id": "323-0", "description": "L-GNC (Servito)"},
                {"id": "324-x", "description": "GNL"},
                {"id": "324-1", "description": "GNL (Self)"},
                {"id": "324-0", "description": "GNL (Servito)"},
            ]
        },
        {
            "results": [
                {
                    "id": 75557219,
                    "price": 2.079,
                    "name": "Benzina",
                    "fuelId": 1,
                    "isSelf": False,
                },
                {
                    "id": 75557218,
                    "price": 1.869,
                    "name": "Benzina",
                    "fuelId": 1,
                    "isSelf": True,
                },
                {
                    "id": 75557221,
                    "price": 1.989,
                    "name": "Gasolio",
                    "fuelId": 2,
                    "isSelf": False,
                },
                {
                    "id": 75557220,
                    "price": 1.779,
                    "name": "Gasolio",
                    "fuelId": 2,
                    "isSelf": True,
                },
            ]
        },
        {
            "results": [
                {
                    "id": 75557219,
                    "price": 2.079,
                    "name": "Benzina",
                    "fuelId": 1,
                    "isSelf": False,
                    "insertDate": "2024-07-02T12:00:38Z",
                    "validityDate": "2024-07-02T11:59:00Z",
                },
                {
                    "id": 75557218,
                    "price": 1.869,
                    "name": "Benzina",
                    "fuelId": 1,
                    "isSelf": True,
                    "insertDate": "2024-07-02T12:00:38Z",
                    "validityDate": "2024-07-02T11:59:00Z",
                },
            ]
        },
    ],
)
async def test_fuels(
    client: Osservaprezzi,
    snapshot: SnapshotAssertion,
) -> None:
    assert snapshot(name="fuels") == await client.get_fuels()
