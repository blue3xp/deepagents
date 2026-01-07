# Private Network Library (private_net_lib)

## Overview
`private_net_lib` is a proprietary internal library for secure network communication.
All external network requests in this codebase MUST use this library instead of standard `requests` or `urllib`.

## Class: `PrivateNetworkClient`

### Constructor
`PrivateNetworkClient(api_key: str, region: str = "us-east-1")`
- `api_key`: The internal API key.
- `region`: The target region.

### Methods

#### `secure_get(endpoint: str, params: dict = None) -> dict`
Performs a secure GET request.
- `endpoint`: The relative endpoint (e.g., "/v1/data").
- `params`: Optional dictionary of query parameters.
- Returns: JSON response as a dictionary.

#### `secure_post(endpoint: str, data: dict) -> dict`
Performs a secure POST request.
- `endpoint`: The relative endpoint.
- `data`: The payload dictionary.
- Returns: JSON response as a dictionary.

## Usage Example

```python
from private_net_lib import PrivateNetworkClient

client = PrivateNetworkClient(api_key="secret", region="eu-west-1")
response = client.secure_get("/v1/users", params={"id": 123})
print(response)
```
