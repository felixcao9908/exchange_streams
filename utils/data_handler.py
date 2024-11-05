import json
import datetime
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
    try:
        bids = [(int(price) / 1e18, int(volume) / 1e18) for price, volume in data['bids']]
        asks = [(int(price) / 1e18, int(volume) / 1e18) for price, volume in data['asks']]
        timestamp = int(data['timestamp']) / 1e6
    except Exception:
        bids = [(int(item['price']) / 1e6, int(item['size']) / 1e6) for item in data['bids'][:1]]
        asks = [(int(item['price']) / 1e6, int(item['size']) / 1e6) for item in data['asks'][:1]]
        timestamp = data['ts']


    return {
        'bids': bids,
        'asks': asks,
        'timestamp_ms': timestamp
    }