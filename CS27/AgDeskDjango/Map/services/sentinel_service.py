from dotenv import load_dotenv
import requests
import os
import time

class SentinelService:
    """
    Service class for managing Sentinel Hub API access tokens and instance IDs.
    Handles automatic retrieval and caching of authentication tokens.
    """

    def __init__(self):
        """
        Load environment variables and initialize token storage.
        """
        load_dotenv()
        self._token = None
        self._token_expiry = 0

    def get_token(self):
        """
        Retrieve a valid access token from Sentinel Hub. Cached if not expired.

        Returns:
            str: A valid access token string.

        Raises:
            HTTPError: If the request to the token endpoint fails.
        """
        now = time.time()
        if self._token and now < self._token_expiry:
            return self._token

        url = "https://services.sentinel-hub.com/oauth/token"
        payload = {
            "grant_type": "client_credentials",
            "client_id": os.getenv("SENTINEL_HUB_CLIENT_ID"),
            "client_secret": os.getenv("SENTINEL_HUB_CLIENT_SECRET")
        }

        response = requests.post(url, data=payload)
        response.raise_for_status()
        token_data = response.json()

        self._token = token_data["access_token"]
        self._token_expiry = now + token_data["expires_in"] - 60

        return self._token

    def get_instance_id(self):
        """
        Get the Sentinel Hub instance ID from environment variables.

        Returns:
            str: Sentinel Hub instance ID.
        """
        return os.getenv("SENTINEL_HUB_INSTANCE_ID")
