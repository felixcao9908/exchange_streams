# arbitrage_calculator.py
import csv
from datetime import datetime
import asyncio
from Vertex_Socket import vertex_data, start_vertex_socket
from drift_socket import drift_data, start_drift_socket


async def calculate_arbitrage():
    # Ensure both Vertex and Drift data are available
    if vertex_data["bids"] is None or drift_data["bids"] is None:
        print("No data yet")
        return

    # Retrieve bid/ask values and timestamps for debugging
    vertex_bid = vertex_data["bids"][0][0]
    vertex_ask = vertex_data["asks"][0][0]
    vertex_time = vertex_data["timestamp_ms"]

    drift_bid = drift_data["bids"][0][0]
    drift_ask = drift_data["asks"][0][0]
    drift_time = drift_data["timestamp_ms"]
    vertex_time_ms = vertex_time / 1e6

    time_difference_ms = abs(vertex_time_ms - drift_time)
    vertex_fee_bps = 2  # 2 bps taker
    drift_fee_bps = 2.125  # Assuming 15% referral rebate

    vertex_bid_adj = vertex_bid * (1 - vertex_fee_bps / 10000)
    vertex_ask_adj = vertex_ask * (1 + vertex_fee_bps / 10000)
    drift_bid_adj = drift_bid * (1 - drift_fee_bps / 10000)
    drift_ask_adj = drift_ask * (1 + drift_fee_bps / 10000)


    # Debug prints to verify data values with timestamps
    print(f"Vertex Bid: {vertex_bid_adj}, Vertex Ask: {vertex_ask_adj}, Vertex Time: {vertex_time}")
    print(f"Drift Bid: {drift_bid_adj}, Drift Ask: {drift_ask_adj}, Drift Time: {drift_time}")
    print(f"Time gap: {time_difference_ms}")
    if vertex_bid_adj > drift_ask_adj:
        print(f"Arbitrage opportunity: Buy on Drift at {drift_ask} and sell on Vertex at {vertex_bid}. "
              f"Profit after fees: {vertex_bid_adj - drift_ask_adj}")
    if drift_bid_adj > vertex_ask_adj:
        print(f"Arbitrage opportunity: Buy on Vertex at {vertex_ask} and sell on Drift at {drift_bid}. "
              f"Profit after fees: {drift_bid_adj - vertex_ask_adj}")
    else:
        print("No arbitrage opportunity detected after accounting for fees.")

async def main_arbitrage():
    vertex_task = asyncio.create_task(start_vertex_socket())
    drift_task = asyncio.create_task(start_drift_socket())

    try:
        while True:
            await calculate_arbitrage()
            await asyncio.sleep(2)
    except KeyboardInterrupt:
        print("Arbitrage calculation stopped.")
    finally:
        vertex_task.cancel()
        drift_task.cancel()

if __name__ == "__main__":
    asyncio.run(main_arbitrage())
