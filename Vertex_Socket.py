import websocket
import json
import base64
import os

def generate_websocket_key():
    # Generate a 16-byte random key and base64 encode it
    key = base64.b64encode(os.urandom(16)).decode("utf-8")
    return key

def subscribe_best_bid_offer():
    # WebSocket URL for Vertex API
    url = "ws://localhost:8080/v1/subscribe"

    # Subscription message for the WebSocket
    subscription_message = json.dumps({
        "method": "subscribe",
        "stream": {
            "type": "best_bid_offer",
            "product_id": 2  # Product ID for BTC-PERP
        },
        "id": 10
    })

    # Define the function to handle incoming messages
    def on_message(ws, message):
        data = json.loads(message)
        bid_price = data.get("bid_price")
        ask_price = data.get("ask_price")
        print(f"Bid Price: {bid_price}, Ask Price: {ask_price}")

    # Define the function to handle errors
    def on_error(ws, error):
        print("Error:", error)

    # Define the function to handle connection close
    def on_close(ws, close_status_code, close_msg):
        print("Connection closed with code:", close_status_code, "Message:", close_msg)

    # Define the function to handle connection open and send the subscription message
    def on_open(ws):
        print("Connection opened")
        ws.send(subscription_message)

    # Manually specify headers, including a generated Sec-WebSocket-Key
    headers = [
        "Host: gateway.base-prod.vertexprotocol.com",
        "Upgrade: websocket",
        "Connection: Upgrade",
        "Sec-WebSocket-Version: 13",
        f"Sec-WebSocket-Key: {generate_websocket_key()}"  # Generate a unique WebSocket key for each connection
    ]

    # Create the WebSocket app
    ws = websocket.WebSocketApp(url,
                                header=headers,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    # Run the WebSocket app
    ws.run_forever()

# Run the function
subscribe_best_bid_offer()
