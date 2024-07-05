"""Helpers definition."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from .models import Brand, Fuel, GPSCoordinates, Marker, Service, Station


def brand_from_json(json: dict[str, Any]) -> Brand:
    """Create a brand from JSON."""
    return Brand(
        id=json.get("bandieraId", ""),
        name=json.get("bandiera", ""),
        markers=[marker_from_json(marker) for marker in json.get("logoMarkerList", [])],
    )


def fuel_from_json(json: dict[str, Any]) -> Fuel:
    """Create a fuel from JSON."""
    return Fuel(
        id=json.get("id", 0),
        price=json.get("price", 0),
        name=json.get("name", json.get("description", "")),
        fuel_id=json.get("fuelId", 0),
        is_self=json.get("isSelf", False),
        insert_date=datetime.fromisoformat(json["insertDate"])
        if "insertDate" in json
        else None,
        validity_date=datetime.fromisoformat(json["validityDate"])
        if "validityDate" in json
        else None,
    )


def gps_coordinates_from_json(json: dict[str, Any]) -> GPSCoordinates:
    """Create a GPS Coordinates from JSON."""
    return GPSCoordinates(
        latitude=json.get("lat", 0),
        longitude=json.get("lng", 0),
    )


def marker_from_json(json: dict[str, Any]) -> Marker:
    """Create a marker from JSON."""
    return Marker(
        type=json.get("tipoFile", ""),
        extension=json.get("estensione", ""),
        content=json.get("content", ""),
    )


def service_from_json(json: dict[str, Any]) -> Service:
    """Create a service from JSON."""
    return Service(
        id=json.get("id", ""),
        description=json.get("description", ""),
    )


def station_from_json(json: dict[str, Any]) -> Station:
    """Create a station from JSON."""
    return Station(
        id=json.get("id", 0),
        name=json.get("name", ""),
        description=json.get("nomeImpianto", ""),
        fuels=[fuel_from_json(fuel) for fuel in json.get("fuels", [])],
        location=gps_coordinates_from_json(json.get("location", {})),
        insert_date=datetime.fromisoformat(json["insertDate"])
        if "insertDate" in json
        else None,
        address=json.get("address"),
        brand=json.get("brand"),
        email=json.get("email"),
        website=json.get("website"),
        phone=json.get("phoneNumber"),
        company=json.get("company"),
        services=[service_from_json(service) for service in json.get("services", [])],
    )
