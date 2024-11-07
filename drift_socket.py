# drift_socket.py
import asyncio
import websockets
import json
from utils.data_handler import parse_drift_data

drift_data = {
    "bids": None,
    "asks": None,
    "timestamp_ms": None
}

async def subscribe_best_bid_offer_drift():
    url = "wss://dlob.drift.trade/ws"
    subscription_message = json.dumps({
        "type": "subscribe",
        "marketType": "perp",
        "channel": "orderbook",
        "market": "BTC-PERP"
    })

    async with websockets.connect(url) as websocket:
        print("Connected to Drift WebSocket")
        await websocket.send(subscription_message)

        while True:
            response = await websocket.recv()
            data = json.loads(response)

            # Parse bids, asks, and timestamp
            if "data" in data:
                orderbook = json.loads(data["data"])  # Load JSON string
                if "bids" in orderbook and "asks" in orderbook:
                    drift_data["bids"] = [(float(orderbook["bids"][0]["price"]) / 1e6, float(orderbook["bids"][0]["size"]) / 1e6)]
                    drift_data["asks"] = [(float(orderbook["asks"][0]["price"]) / 1e6, float(orderbook["asks"][0]["size"]) / 1e6)]
                    
                    
                    drift_data["timestamp_ms"] = int(orderbook["ts"])
                    # print("Updated Drift data:", drift_data)  # For debugging, remove if unnecessary
            else:
                print("Drift WebSocket message received:", data)  # Only print if data is unexpected

async def start_drift_socket():
    await subscribe_best_bid_offer_drift()
