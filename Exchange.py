import websocket
import websockets
import json
import asyncio


class Exchange:
    def __init__(self, name, _websocket, rest_endpoint):
        self.name = name
        self.websocket = _websocket
        self.rest_endpoint = rest_endpoint

    def get_name(self):
        return self.name

    def get_websocket(self):
        return self.websocket

    def get_rest_endpoint(self):
        return self.rest_endpoint


class Product(Exchange):
    def __init__(self, name, websocket, rest_endpoint, message,  product_id, depth, suffix):
        super().__init__(name, websocket, rest_endpoint)
        self.product_id = product_id
        self.depth = depth
        self.message = message
        self.data = {
            "bids": None,
            "asks": None,
            "timestamp_ms": None
        }
        self.suffix = suffix

    def get_product_id(self):
        return self.product_id

    def get_depth(self):
        return self.depth

    async def start_vertex_socket(self):
        await self.subscribe_best_bid_offer()

    async def subscribe_best_bid_offer(self):
        async with websockets.connect(self.websocket) as websocket:
            print("Connected to Vertex WebSocket")
            await websocket.send(self.message)

            while True:
                response = await websocket.recv()
                data = json.loads(response)

                # Check for and parse bid/ask fields directly
                if "bid_price" in data and "ask_price" in data:
                    self.data["bids"] = [(float(data["bid_price"]) / self.suffix, float(data["bid_qty"]) / self.suffix)]
                    self.data["asks"] = [(float(data["ask_price"]) / self.suffix, float(data["ask_qty"]) / self.suffix)]
                    self.data["timestamp_ms"] = int(data["timestamp"])
                    # print("Updated Vertex data:", vertex_data)  # For debugging, remove if unnecessary
                else:
                    print("Vertex WebSocket message received:", self.data)  # Only print if data is unexpected

