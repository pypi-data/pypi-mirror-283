from typing import Any, Dict, List

import httpx


class PropertiaClient:
    SMARTSCORE_ENDPOINT = '/smartscore/'
    ISOCHRONES_ENDPOINT = '/isochrones/'
    COMMUTE_TIME_ENDPOINT = '/commute-time/'
    USER_CATEGORIES_ENDPOINT = '/user-categories/'

    def __init__(self, api_key: str, host: str = "https://propertia.searchsmartly.co") -> None:
        self._host = host.rstrip("/")
        self._api_key = api_key
        self._headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        self.client = httpx.Client(
            transport=httpx.HTTPTransport(retries=3),
            base_url=self._host,
            headers=self._headers,
            timeout=httpx.Timeout(connect=None, read=None, write=None, pool=None)
        )

    def add_header(self, key: str, value: str) -> None:
        self._headers[key] = value

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def get_scores(self, properties: List, needs: Dict[str, Any], region: str = "World") -> Dict[str, List]:
        payload = {
            "needs": needs,
            "properties": properties,
        }
        self.add_header("X-Region", region)
        return self.make_post_call(self.SMARTSCORE_ENDPOINT, payload)

    def get_isochrones(self, destinations: List, aggregated: bool) -> Dict[str, Any]:
        """
        The destinations parameter is a list of 1 or 2 dictionaries, each of which must contain the following:
        {
            "id": "destination",
            "latitude": 25.197197,
            "longitude": 55.27437639999999,
            "time": 10,
            "methods": [
                "walking", "driving", "cycling", "public_transport"
            ]
        }
        The aggregated parameter is a boolean that specifies whether to return a single isochrone or a list of them
        """
        payload = {
            "destinations": destinations,
            "aggregated": aggregated
        }
        return self.make_post_call(self.ISOCHRONES_ENDPOINT, payload)

    def get_commute_time(self, destinations: List, properties: List) -> Dict[str, List]:
        """
        The destinations parameter is a list of 1 or 2 dictionaries, each of which must contain the following:
        {
            "id": "destination",
            "latitude": 25.197197,
            "longitude": 55.27437639999999,
            "time": 10,
            "methods": [
                "walking", "driving", "cycling", "public_transport"
            ]
        }
        The properties parameter is a list of dictionaries, each of which must contain the following:
        {
            "id": "string",
            "latitude": -90,
            "longitude": -180
        }
        """
        payload = {
            "destinations": destinations,
            "properties": properties,
        }
        return self.make_post_call(self.COMMUTE_TIME_ENDPOINT, payload)

    def make_post_call(self, endpoint: str, payload: Dict) -> Dict[str, List]:
        return self.client.post(endpoint, json=payload).json()

    def get_user_categories(self) -> Dict[str, List]:
        return self.make_get_call(self.USER_CATEGORIES_ENDPOINT)

    def make_get_call(self, endpoint: str) -> Dict[str, List]:
        return self.client.get(endpoint).json()
