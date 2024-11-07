# drift_socket.py
import asyncio
import websockets
import json

drift_data = {
    "bid_price": None,
    "bid_qty": None,
    "ask_price": None,
    "ask_qty": None
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

            # Debugging output
            print("Received data from Drift:", data)

            # Update bid and ask data
            drift_data["bid_price"] = float(data.get("bid_price"))
            drift_data["bid_qty"] = float(data.get("bid_qty"))
            drift_data["ask_price"] = float(data.get("ask_price"))
            drift_data["ask_qty"] = float(data.get("ask_qty"))

            # Confirm updated data
            print("Updated Drift data:", drift_data)

async def start_drift_socket():
    await subscribe_best_bid_offer_drift()
