import requests, os, time
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 文件

# 全局缓存变量
_token = None
_token_expiry = 0

  # 预加载 token
def get_sentinel_token():
    global _token, _token_expiry

    now = time.time()
    if _token and now < _token_expiry:
        return _token  # 如果还没过期，直接返回

    # 否则重新获取 token
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
    _token_expiry = now + token_data["expires_in"] - 60  # 提前60秒过期防止边界问题

    print(_token)
    return _token

token= get_sentinel_token()