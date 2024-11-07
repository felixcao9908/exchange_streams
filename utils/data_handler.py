# data_handler.py
import json

def parse_vertex_data(data: dict) -> dict:
    """
    Parses Vertex liquidity data from WebSocket and converts from fixed-point to decimal.
    """
    if 'data' in data:
        try:
            data = json.loads(data['data'])
        except Exception as e:
            raise ValueError(f"Failed to parse JSON data: {e}")
    bids = [(int(price) / 1e18, int(volume) / 1e18) for price, volume in data['bids']]
    asks = [(int(price) / 1e18, int(volume) / 1e18) for price, volume in data['asks']]
    timestamp = int(data['timestamp']) / 1e6
    return {
        'bids': bids,
        'asks': asks,
        'timestamp_ms': timestamp
    }

def parse_drift_data(data: dict) -> dict:
    """
    Parses Drift liquidity data from WebSocket and converts from fixed-point to decimal.
    """
    bids = [(int(item['price']) / 1e6, int(item['size']) / 1e6) for item in data['bids'][:1]]
    asks = [(int(item['price']) / 1e6, int(item['size']) / 1e6) for item in data['asks'][:1]]
    timestamp = data['ts']
    return {
        'bids': bids,
        'asks': asks,
        'timestamp_ms': timestamp
    }
