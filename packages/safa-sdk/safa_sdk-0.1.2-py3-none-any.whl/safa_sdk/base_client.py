from typing import Any, Dict, Optional

import requests


class BaseClient:
    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url
        self.headers = headers if headers else {}

        self.session = requests.Session()

    def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        url = f"{self.base_url}/{endpoint}"
        response = self.session.request(method, url, headers=self.headers, **kwargs)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise Exception(f"HTTP error occurred: {e}")

        if response.status_code != 204:  # No Content
            return response.json()
        return None

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Any:
        return self._request("POST", endpoint, json=data)

    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Any:
        return self._request("PUT", endpoint, json=data)

    def delete(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Any:
        return self._request("DELETE", endpoint, json=data)

    def get_cookie(self, cookie_name: str, error: str = None):
        if error is None:
            error = f"Could not find cookie {cookie_name}"
        if cookie_name not in self.session.cookies:
            raise Exception(error)
        return self.session.cookies[cookie_name]

    def set_auth_cookie(self, token: str) -> None:
        self.session.cookies.set('SAFA-TOKEN', token)
