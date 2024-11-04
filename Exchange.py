import websocket
class Exchange:
    def __init__(self, name, websocket_endpoint, rest_endpoint):
        self.name = name
        self.websocket = websocket.WebSocket()
        self.websocket.connect(websocket_endpoint)
        self.websocket_endpoint = websocket_endpoint
        self.rest_endpoint = rest_endpoint

    def get_name(self):
        return self.name
    def get_websocket_endpoint(self):
        return self.websocket_endpoint

    def get_rest_endpoint(self):
        return self.rest_endpoint


class Product(Exchange):
    def __init__(self, name, websocket_endpoint, rest_endpoint, product_id, depth):
        super().__init__(name, websocket_endpoint, rest_endpoint)
        self.product_id = product_id
        self.depth = depth

    def get_product_id(self):
        return self.product_id

    def get_depth(self):
        return self.depth
