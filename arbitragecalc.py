# arbitrage_calculator.py
import json
from main import main
import time

def calculate_arbitrage(parsed_data_vertex, parsed_data_drift):
    vertex_bid = parsed_data_vertex["bids"][0][0]
    vertex_ask = parsed_data_vertex["asks"][0][0]
    drift_bid = parsed_data_drift["bids"][0][0]
    drift_ask = parsed_data_drift["asks"][0][0]

    # Define fees as basis points (bps)
    vertex_fee_bps = 6  # 6 bps
    drift_fee_bps = 2.5  # 2.5 bps

    # Convert bps to decimal and calculate adjusted prices after fees
    vertex_bid_adj = vertex_bid * (1 - vertex_fee_bps / 10000)
    vertex_ask_adj = vertex_ask * (1 + vertex_fee_bps / 10000)
    drift_bid_adj = drift_bid * (1 - drift_fee_bps / 10000)
    drift_ask_adj = drift_ask * (1 + drift_fee_bps / 10000)

    # Check for arbitrage opportunities with fee-adjusted prices
    if vertex_bid_adj > drift_ask_adj:
        print(f"Arbitrage opportunity: Buy on Drift at {drift_ask} and sell on Vertex at {vertex_bid}. "
              f"Profit after fees: {vertex_bid_adj - drift_ask_adj}")
    elif drift_bid_adj > vertex_ask_adj:
        print(f"Arbitrage opportunity: Buy on Vertex at {vertex_ask} and sell on Drift at {drift_bid}. "
              f"Profit after fees: {drift_bid_adj - vertex_ask_adj}")
    else:
        print("No arbitrage opportunity detected after accounting for fees.")


def main_arbitrage():
    i = 0
    while i <= 2:
        # Run the main function from main.py to get parsed data
        start_time =time.time()
        parsed_data = main()
        end_time = time.time()

        
        # Unpack parsed data for Vertex and Drift
        parsed_data_vertex = parsed_data['vertex']
        parsed_data_drift = parsed_data['drift']

        # Calculate arbitrage
        calculate_arbitrage(parsed_data_vertex, parsed_data_drift)
        

        print(f"Execution time: {end_time - start_time:.6f} seconds")

        i += 1

if __name__ == "__main__":
    main_arbitrage()
