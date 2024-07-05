"""Models module."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime


@dataclass(frozen=True)
class GPSCoordinates:
    """GPS coordinates definition."""

    latitude: float
    longitude: float

    def to_json(self) -> dict[str, float]:
        """Return JSON representation of the object."""
        return {
            "lat": self.latitude,
            "lng": self.longitude,
        }


@dataclass(frozen=True)
class Fuel:
    """Fuel definition."""

    id: int
    price: float
    name: str
    fuel_id: int
    is_self: bool
    insert_date: datetime | None
    validity_date: datetime | None


@dataclass(frozen=True)
# pylint: disable-next=too-many-instance-attributes
class Station:
    """Station definition."""

    id: int
    name: str
    description: str
    fuels: list[Fuel]
    location: GPSCoordinates
    insert_date: datetime | None
    address: str | None
    brand: str | None
    email: str | None
    website: str | None
    phone: str | None
    company: str | None
    services: list[Service] | None


@dataclass(frozen=True)
class Marker:
    """Marker definition."""

    type: str
    extension: str
    content: str


@dataclass(frozen=True)
class Brand:
    """Brand definition."""

    id: int
    name: str
    markers: list[Marker]


@dataclass(frozen=True)
class Service:
    """Service definition."""

    id: str | int
    description: str
