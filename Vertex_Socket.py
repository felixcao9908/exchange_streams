# vertex_socket.py
import asyncio
import websockets
import json

vertex_data = {
    "bids": None,
    "asks": None,
    "timestamp_ms": None
}

async def subscribe_best_bid_offer_vertex():
    url = "wss://gateway.prod.vertexprotocol.com/v1/subscribe"
    subscription_message = json.dumps({
        "method": "subscribe",
        "stream": {
            "type": "best_bid_offer",
            "product_id": 2  # BTC-PERP product ID
        },
        "id": 10
    })

    async with websockets.connect(url) as websocket:
        print("Connected to Vertex WebSocket")
        await websocket.send(subscription_message)

        while True:
            response = await websocket.recv()
            data = json.loads(response)

            # Check for and parse bid/ask fields directly
            if "bid_price" in data and "ask_price" in data:
                vertex_data["bids"] = [(float(data["bid_price"]) / 1e18, float(data["bid_qty"]) / 1e18)]
                vertex_data["asks"] = [(float(data["ask_price"]) / 1e18, float(data["ask_qty"]) / 1e18)]
                vertex_data["timestamp_ms"] = int(data["timestamp"])
                # print("Updated Vertex data:", vertex_data)  # For debugging, remove if unnecessary
            else:
                print("Vertex WebSocket message received:", data)  # Only print if data is unexpected

async def start_vertex_socket():
    await subscribe_best_bid_offer_vertex()
