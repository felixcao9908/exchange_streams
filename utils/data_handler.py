import json
def parse_liquidity_data(data: dict) -> dict:
    """
    Parses and converts the liquidity data from fixed-point to decimal.

    Args:
        data (dict): Raw liquidity data from the API.

    Returns:
        dict: Parsed data with decimal prices and sizes.
    """
    if 'data' in data:
        try:
            data = json.loads(data['data'])
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON data: {e}")

    bids = [(int(item['price']) / 1e18, int(item['size']) / 1e18) for item in data['bids']]
    asks = [(int(item['price']) / 1e18, int(item['size']) / 1e18) for item in data['asks']]
    timestamp_ns = int(data['ts'])
    return {
        'bids': bids,
        'asks': asks,
        'timestamp_ns': timestamp_ns
    }