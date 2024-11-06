import asyncio
import websockets
import json


async def subscribe_best_bid_ask():
    url = "wss://dlob.drift.trade/ws"  # Drift Protocol WebSocket URL
    market = "BTC-PERP"  # Market to subscribe to

    async with websockets.connect(url) as ws:
        # Subscription message for the BTC-PERP order book
        subscription_message = json.dumps({
            "type": "subscribe",
            "marketType": "perp",
            "channel": "orderbook",
            "market": market
        })

        await ws.send(subscription_message)
        print(f"Subscription sent to Drift Protocol WebSocket for {market}")

        # Listen for incoming messages and extract best bid/ask for BTC-PERP
        async for message in ws:
            data = json.loads(message)

            # Check if we have the correct channel and market
            if data.get("channel") == "orderbook_perp_1" and "data" in data:
                # Convert the inner string to a dictionary
                inner_data = json.loads(data["data"])

                # Filter out only the best bid and ask
                bids = inner_data.get("bids", [])
                asks = inner_data.get("asks", [])

                # Get the best bid and ask if they exist
                if bids and asks:
                    best_bid = bids[0]
                    best_ask = asks[0]
                    bid_price = best_bid["price"]
                    ask_price = best_ask["price"]
                    quant = best_bid["size"]

                    # Print bid, ask, and quantity on the same line
                    print(f"Bid: {bid_price}, Ask: {ask_price}, Quant: {quant}")
            else:
                # Ignore all other types of messages
                continue


# Run the WebSocket connection
asyncio.run(subscribe_best_bid_ask())
