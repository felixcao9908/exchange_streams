import requests
import json
import toml
import data_connection.api_connection as apc
import utils.data_handler as dh
from Exchange import Product
import websocket

config = toml.load('config.toml')
env = 'testnet'

# Initialize WebSocket connection
ws_vertex = websocket.WebSocket()
ws_vertex.connect(config['vertex'][env]['blast_sepolia']['gateway_ws'])

ws_drift = websocket.WebSocket()
ws_drift.connect(config['drift'][env]['gateway_ws'])

# Initialize Product objects with WebSocket connections
Vertex = Product('Vertex', config['vertex'][env]['blast_sepolia']['gateway_ws'], config['vertex'][env]['blast_sepolia']['gateway_rest'], 2, 5)
Drift = Product('Drift', config['drift'][env]['gateway_ws'], None, "BTC-PERP", None)

def main():
    raw_data_vertex = apc.get_market_liquidity(Vertex)
    raw_data_drift = apc.get_market_liquidity(Drift)
    parsed_data_vertex = dh.parse_liquidity_data(raw_data_vertex)
    parsed_data_drift = dh.parse_liquidity_data(raw_data_drift)
    print(json.dumps(parsed_data_vertex, indent=2))
    print(json.dumps(parsed_data_drift, indent=2))

if __name__ == "__main__":
    main()