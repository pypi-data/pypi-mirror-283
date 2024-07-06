import time
from typing import Any, List, Optional

import requests
from corehttp.credentials import AccessToken, TokenCredential

from ._logger import logger


class MachineTokenCredential(TokenCredential):
    def __init__(self, client_id: str, client_secret: str, auth_endpoint: str, scopes: List[str]):
        self.url = auth_endpoint
        self._access_token = None
        self.request_data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
            "scope": " ".join(scopes),
        }

    def get_token(self, *scopes: str, claims: Optional[str] = None, **kwargs: Any) -> AccessToken:
        logger.info(f"Getting access token using client_credentials from {self.url}")

        data = {"scope": " ".join(["trapi"]), **self.request_data}

        response = requests.post(self.url, data=data)

        if response.status_code != 200:
            raise RuntimeError(
                f"Failed to get access token. Response code: {response.status_code}. Response: {response.text}"
            )

        access_token = response.json().get("access_token")
        expires_in = response.json().get("expires_in")

        if not access_token:
            raise RuntimeError(
                f"Failed to get access token. Successful response, but no access token found. Response: {response.text}"
            )

        logger.info("Access token retrieved successfully")

        return AccessToken(token=access_token, expires_on=time.time() + expires_in)
