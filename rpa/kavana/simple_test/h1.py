import ssl
import requests
from urllib3.poolmanager import PoolManager
from requests.adapters import HTTPAdapter

class SecureTLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.minimum_version = ssl.TLSVersion.TLSv1_2  # 최소 TLS 1.2
        kwargs["ssl_context"] = context
        return super().init_poolmanager(*args, **kwargs)

session = requests.Session()
session.mount("https://", SecureTLSAdapter())

response = session.get(
    "https://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getAnniversaryInfo",
    params={
        "ServiceKey": "1ROBN6Q1t6iYO9fc2SbHVby0AruUb78/jd0Ruzvyv33tgJKV7WcOyZ+SmhnNPIYmrR0/ppqifPYDcrywywu9ZQ==",
        "pageNo": 1,
        "numOfRows": 10,
        "solYear": 2025,
        "solMonth": 4
    },
    headers={
        "User-Agent": "Mozilla/5.0"
    },
    timeout=10
)

print(response.status_code)
print(response.text[:300])
