import timeit
from functools import cache
import asyncio
import ssl

import requests
import websockets
import websocket
import json
from Exchange import Product


@cache
def get_url(Product: Product) -> str:
    """
    Returns the URL for a specified product.

    Args:
        Product (Product): Product object containing exchange and product information.

    Returns:
        str: URL for the specified product.
    """
    if Product.get_name() == 'Vertex':
        endpoint = Product.get_websocket()
        url = endpoint
        # endpoint = Product.get_rest_endpoint()
        # url = f"{endpoint}/query"
    elif Product.get_name() == 'Drift':
        endpoint = Product.get_websocket()
        url = endpoint
    else:
        raise ValueError(f"Invalid product: {Product.get_name()}")
    return url


@cache
def get_params(Product: Product) -> dict:
    """
    Returns the parameters for a specified product.

    Args:
        Product (Product): Product object containing exchange and product information.

    Returns:
        dict: Parameters for the specified product.
    """
    if Product.get_name() == 'Vertex':
        params = {
            "method": "subscribe",
            "stream": {
                "type": "best_bid_offer",
                "product_id": 2  # BTC-PERP product ID
            },
            "id": 10
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




def get_market_liquidity_drift(Product: Product) -> dict:
    """
    Fetches market liquidity data for a specified product and depth.

    Args:
        Product (Product): Product object containing exchange and product information.

    Returns:
        dict: Parsed JSON response containing bids, asks, and timestamp.
    """
    params = get_params(Product)
    try:
        ws = Product.get_websocket()
        ws.send(json.dumps(params))
        while True:
            response = ws.recv()
            temp = json.loads(response)
            if 'data' in temp:
                return temp
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"Request failed: {e}")
    except websocket.WebSocketException as e:
        raise SystemExit(f"WebSocket request failed: {e}")


def get_market_liquidity_vertex(Product: Product) -> dict:
    """
    Fetches market liquidity data for a specified product and depth.

    Args:
        Product (Product): Product object containing exchange and product information.

    Returns:
        dict: Parsed JSON response containing bids, asks, and timestamp.
    """
    params = json.dumps({
        "method": "subscribe",
        "stream": {
            "type": "best_bid_offer",
            "product_id": 2  # BTC-PERP product ID
        },
        "id": 10
    })
    url = "wss://gateway.prod.vertexprotocol.com/v1/subscribe"

    ssl_context = ssl.SSLContext()
    try:
        ws = websocket.create_connection(url, sslopt={"cert_reqs": ssl.CERT_NONE}, header=["Sec-WebSocket-Extensions: permessage-deflate"])
        ws.send(params)
        while True:
            response = ws.recv()
            data = json.loads(response)
            if 'type' in data:
                return data
    except Exception as e:
        raise SystemExit(f"Request failed: {e}")


