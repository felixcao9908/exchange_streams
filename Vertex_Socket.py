# vertex_socket.py
import asyncio
import websockets
import json

vertex_data = {
    "bid_price": None,
    "bid_qty": None,
    "ask_price": None,
    "ask_qty": None
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
            
            # Debugging output
            print("Received data from Vertex:", data)

            # Update bid and ask data with scaling
            vertex_data["bid_price"] = float(data.get("bid_price")) / 1e18
            vertex_data["bid_qty"] = float(data.get("bid_qty")) / 1e18
            vertex_data["ask_price"] = float(data.get("ask_price")) / 1e18
            vertex_data["ask_qty"] = float(data.get("ask_qty")) / 1e18

            # Confirm updated data
            print("Updated Vertex data:", vertex_data)

async def start_vertex_socket():
    await subscribe_best_bid_offer_vertex()
