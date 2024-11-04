import requests
import websocket
import json
from Exchange import Product

def get_url(Product: Product) -> str:
    """
    Returns the URL for a specified product.

    Args:
        Product (Product): Product object containing exchange and product information.

    Returns:
        str: URL for the specified product.
    """
    if Product.get_name() == 'Vertex':
        endpoint = Product.get_rest_endpoint()
        url = f"{endpoint}/query"
    elif Product.get_name() == 'Drift':
        endpoint = Product.get_websocket_endpoint()
        url = endpoint
    else:
        raise ValueError(f"Invalid product: {Product.get_name()}")
    return url

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

def get_market_liquidity(Product: Product) -> dict:
    """
    Fetches market liquidity data for a specified product and depth.

    Args:
        Product (Product): Product object containing exchange and product information.

    Returns:
        dict: Parsed JSON response containing bids, asks, and timestamp.
    """
    url = get_url(Product)
    params = get_params(Product)
    try:
        if Product.get_name() == 'Vertex':
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            if data['status'] == 'success':
                return data['data']
            else:
                raise ValueError(f"API error: {data}")
        elif Product.get_name() == 'Drift':
            ws = Product.websocket
            ws.connect(url)
            ws.send(json.dumps(params))
            i = 0
            while True:
                response = ws.recv()
                if response:
                    data = json.loads(response)
                else:
                    print("Error receiving message")
                if i == 2:
                    return data
                i += 1
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"Request failed: {e}")
    except websocket.WebSocketException as e:
        raise SystemExit(f"WebSocket request failed: {e}")