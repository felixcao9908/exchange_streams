from functools import cache
import requests
import json
from Exchange import Product

@cache
def get_url(Product: Product) -> str:
    if Product.get_name() == 'Vertex':
        endpoint = Product.get_rest_endpoint()
        url = f"{endpoint}/query"
    elif Product.get_name() == 'Drift':
        endpoint = Product.get_websocket()
        url = endpoint
    else:
        raise ValueError(f"Invalid product: {Product.get_name()}")
    return url

@cache
def get_params(Product: Product) -> dict:
    if Product.get_name() == 'Vertex':
        params = {
            'type': 'market_liquidity',
            'product_id': Product.get_product_id(),
            'depth': Product.get_depth()
        }
    elif Product.get_name() == 'Drift':
        params = {
            "type": "subscribe",
            "marketType": "perp",
            "channel": "orderbook",
            "market": Product.get_product_id()
        }
    else:
        raise ValueError(f"Invalid product: {Product.get_name()}")
    return params

def get_market_liquidity_vertex(Product: Product) -> dict:
    url = get_url(Product)
    params = get_params(Product)
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data['status'] == 'success':
            return data['data']
        else:
            raise ValueError(f"API error: {data}")
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"Request failed: {e}")

# Removed WebSocket handling, which will be handled in vertex_socket.py and drift_socket.py
