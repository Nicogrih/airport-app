from typing import Any

import httpx


class APIClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def get(self, path: str) -> httpx.Response:
        return httpx.get(f"{self.base_url}{path}", timeout=10)

    def post(self, path: str, json: dict[str, Any]) -> httpx.Response:
        return httpx.post(f"{self.base_url}{path}", json=json, timeout=10)

    def put(self, path: str, json: dict[str, Any]) -> httpx.Response:
        return httpx.put(f"{self.base_url}{path}", json=json, timeout=10)

    def delete(self, path: str) -> httpx.Response:
        return httpx.delete(f"{self.base_url}{path}", timeout=10)
