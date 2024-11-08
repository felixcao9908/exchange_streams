import requests
import json
import toml
import asyncio
import ssl
import timeit
import data_connection.api_connection as apc
import utils.data_handler as dh
from Exchange import Product
import websocket

config = toml.load('config.toml')
env = 'mainnet'

# Initialize WebSocket connection
# ws_vertex = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
# ws_vertex.connect(config['vertex'][env]['arbitrum_one']['subscriptions'])
ws_vertex = None

ws_drift = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
ws_drift.connect(config['drift'][env]['gateway_ws'])

# Initialize Product objects with WebSocket connections
Vertex = Product('Vertex', ws_vertex, config['vertex'][env]['arbitrum_one']['gateway_rest'], 2, 1)
Drift = Product('Drift', ws_drift, None, "BTC-PERP", None)





def main():
    i = 0
    while i <= 10:
        start = timeit.default_timer()
        raw_data_vertex = apc.get_market_liquidity_vertex(Vertex),
        raw_data_drift = apc.get_market_liquidity_drift(Drift)
        end = timeit.default_timer()
        print(f"Time taken: {end - start}")
        parsed_data_vertex = dh.parse_liquidity_data(raw_data_vertex, Vertex)
        parsed_data_drift = dh.parse_liquidity_data(raw_data_drift, Drift)
        print(json.dumps(parsed_data_vertex, indent=2))
        print(json.dumps(parsed_data_drift, indent=2))
        i += 1
    #return {"vertex": parsed_data_vertex, "drift": parsed_data_drift}


if __name__ == "__main__":
    main()
