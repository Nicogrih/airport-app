from typing import Any

from app.crud.httpx_client import APIClient

def list_airlines(client:APIClient) -> list[dict[str, any]]:
    """lista de todas la aerolineas"""
    r = client.get("/airlines")
    r.raise_for_status()
    return r.json()

def get_airline(client:APIClient, airline_id :str) ->list[dict[str, any]]:
    r = client.get(f"/airlines/{airline_id}")
    r.raise_for_status()
    return r.json()

def create_airline(client:APIClient,payload: dict[str, Any]) -> dict[str, Any]:
    r = client.post("/airlines", json=payload)
    r.raise_for_status()
    return r.json()

def update_airline(client: APIClient, airline_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    r = client.put(f"/airlines{airline_id}", json=payload)
    r.raise_for_status()
    return r.json()

def delete_airline(client: APIClient, airline_id: str) -> None:
    r = client.delete(f"/airlines/{airline_id}")
    r.raise_for_status()

