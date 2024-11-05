import json
import datetime
import timeit
from Exchange import Product


def parse_liquidity_data(data: dict, Product: Product) -> dict:
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
        except Exception as e:
            raise ValueError(f"Failed to parse JSON data: {e}")
    if Product.get_name() == 'Vertex':
        bids = (int(data.get("bid_price"))/1e18, int(data.get("bid_qty"))/1e18)
        asks = (int(data.get("ask_price"))/1e18, int(data.get("ask_qty"))/1e18)
        timestamp = int(data.get('timestamp')) / 1e6
    else:
        bids = [(int(item['price']) / 1e6, int(item['size']) / 1e6) for item in data['bids'][:1]]
        asks = [(int(item['price']) / 1e6, int(item['size']) / 1e6) for item in data['asks'][:1]]
        timestamp = data['ts']
    return {
        'bids': bids,
        'asks': asks,
        'timestamp_ms': timestamp
    }
