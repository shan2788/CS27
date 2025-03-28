import requests, os, time
from dotenv import load_dotenv

load_dotenv()
_token = None
_token_expiry = 0

def get_sentinel_instance_id():
    return os.getenv("SENTINEL_HUB_INSTANCE_ID")

def get_sentinel_token():
    global _token, _token_expiry

    now = time.time()
    if _token and now < _token_expiry:
        return _token  # if not expired, return directly

    # get a new token
    url = "https://services.sentinel-hub.com/oauth/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": os.getenv("SENTINEL_HUB_CLIENT_ID"),
        "client_secret": os.getenv("SENTINEL_HUB_CLIENT_SECRET")
    }

    response = requests.post(url, data=payload)
    response.raise_for_status()
    token_data = response.json()

    _token = token_data["access_token"]
    _token_expiry = now + token_data["expires_in"] - 60

    return _token