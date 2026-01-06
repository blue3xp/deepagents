class PrivateNetworkClient:
    """Mock Private Network Library"""
    def __init__(self, api_key: str, region: str = "us-east-1"):
        self.api_key = api_key
        self.region = region

    def secure_get(self, endpoint: str, params: dict = None) -> dict:
        print(f"[PrivateNet] GET {endpoint} params={params}")
        return {"status": "ok", "data": "mock_data"}

    def secure_post(self, endpoint: str, data: dict) -> dict:
        print(f"[PrivateNet] POST {endpoint} data={data}")
        return {"status": "created", "id": 999}
