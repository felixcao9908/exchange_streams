# main.py
import asyncio
import json
import toml
from Exchange import Product
from arbitrage_calculator import main_arbitrage

config = toml.load('config.toml')
env = 'mainnet'

# Initialize WebSocket connection
# ws_vertex = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
ws_vertex_url = config['vertex'][env]['arbitrum_one']['subscriptions']
vertex_message = json.dumps({
        "method": "subscribe",
        "stream": {
            "type": "best_bid_offer",
            "product_id": 2  # BTC-PERP product ID
        },
        "id": 10
    })
rp_vertex = None
vertex_suffix = 1e18

ws_drift_ws_url = config['drift'][env]['gateway_ws']
drift_message = json.dumps({
        "type": "subscribe",
        "marketType": "perp",
        "channel": "orderbook",
        "market": "BTC-PERP"
    })
rp_drift = None
drift_suffix = 1e6

# Initialize Product objects
Vertex = Product('Vertex', ws_vertex_url, None, vertex_message, 2, 1, vertex_suffix)
Drift = Product('Drift', ws_drift_ws_url, None, drift_message, "BTC-PERP", None, drift_suffix)
exchanges = [Vertex, Drift]

# Run the main arbitrage function
if __name__ == "__main__":
    asyncio.run(main_arbitrage(exchanges))
