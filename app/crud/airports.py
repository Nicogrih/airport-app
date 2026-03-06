from typing import Any
from app.crud.httpx_client import APIClient

def list_airports(client: APIClient) -> list[dict[str, Any]]:
    """Obtiene la lista de todos los aeropuertos """
    r = client.get("/airports")
    r.raise_for_status()
    return r.json()


def get_airport(client: APIClient, airport_id: str) -> dict[str, Any]:
    r = client.get(f"/airports/{airport_id}")
    r.raise_for_status()
    return r.json()


def create_airport(client: APIClient, payload: dict[str, Any]) -> dict[str, Any]:
    r = client.post("/airports", json=payload)
    r.raise_for_status()
    return r.json()


def update_airport(client: APIClient, airport_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    r = client.put(f"/airports/{airport_id}", json=payload)
    r.raise_for_status()
    return r.json()


def delete_airport(client: APIClient, airport_id: str) -> dict[str, str]:
    r = client.delete(f"/airports/{airport_id}")
    r.raise_for_status()
    return r.json()  