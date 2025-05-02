# services/sentinel_service.py
from dotenv import load_dotenv
import requests
import os
import time

class SentinelService:
    def __init__(self):
        load_dotenv()
        self._token = None
        self._token_expiry = 0

    def get_token(self):
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
        return os.getenv("SENTINEL_HUB_INSTANCE_ID")