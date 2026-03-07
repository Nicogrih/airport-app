from typing import Any
from app.crud.http_client import APIClient


def list_passengers(client: APIClient) -> list[dict[str, Any]]:
    r = client.get("/api/passengers")
    r.raise_for_status()
    return r.json()


def get_passenger(client: APIClient, passenger_id: str) -> dict[str, Any]:
    r = client.get(f"/api/passengers/{passenger_id}")
    r.raise_for_status()
    return r.json()


def create_passenger(
    client: APIClient, payload: dict[str, Any]
) -> dict[str, Any]:
    r = client.post("/api/passengers", json=payload)
    r.raise_for_status()
    return r.json()


def update_passenger(
    client: APIClient, passenger_id: str, payload: dict[str, Any]
) -> dict[str, Any]:
    r = client.put(f"/api/passengers/{passenger_id}", json=payload)
    r.raise_for_status()
    return r.json()


def delete_passenger(client: APIClient, passenger_id: str) -> None:
    r = client.delete(f"/api/passengers/{passenger_id}")
    r.raise_for_status()