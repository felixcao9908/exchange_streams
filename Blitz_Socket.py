import asyncio
import websockets
import json

async def subscribe_best_bid_offer():
    url = "wss://gateway.blast-prod.vertexprotocol.com/v1/subscribe"
    subscription_message = json.dumps({
        "method": "subscribe",
        "stream": {
            "type": "best_bid_offer",
            "product_id": 2  # BTC-PERP product ID
        },
        "id": 10
    })

    async with websockets.connect(url) as websocket:
        await websocket.send(subscription_message)

        while True:
            response = await websocket.recv()
            data = json.loads(response)

            # Extract and print bid and ask prices and quantities
            bid_price = data.get("bid_price")
            bid_qty = data.get("bid_qty")
            ask_price = data.get("ask_price")
            ask_qty = data.get("ask_qty")

            print(f"Bid Price: {bid_price}, Bid Qty: {bid_qty}, Ask Price: {ask_price}, Ask Qty: {ask_qty}")

# Run the asynchronous function
asyncio.run(subscribe_best_bid_offer())
