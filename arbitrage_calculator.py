# arbitrage_calculator.py
import asyncio
from vertex_socket import vertex_data, start_vertex_socket
from drift_socket import drift_data, start_drift_socket

async def calculate_arbitrage():
    # Print vertex and drift data for debugging
    print("Current Vertex Data:", vertex_data)
    print("Current Drift Data:", drift_data)
    
    if vertex_data["bid_price"] is None or drift_data["bid_price"] is None:
        print("Waiting for data from Vertex and Drift...")
        return

    vertex_bid = vertex_data["bid_price"]
    vertex_ask = vertex_data["ask_price"]
    drift_bid = drift_data["bid_price"]
    drift_ask = drift_data["ask_price"]

    vertex_fee_bps = 4  # 4 bps total
    drift_fee_bps = 5  # 5 bps total

    vertex_bid_adj = vertex_bid * (1 - vertex_fee_bps / 10000)
    vertex_ask_adj = vertex_ask * (1 + vertex_fee_bps / 10000)
    drift_bid_adj = drift_bid * (1 - drift_fee_bps / 10000)
    drift_ask_adj = drift_ask * (1 + drift_fee_bps / 10000)

    if vertex_bid_adj > drift_ask_adj:
        print(f"Arbitrage opportunity: Buy on Drift at {drift_ask} and sell on Vertex at {vertex_bid}. "
              f"Profit after fees: {vertex_bid_adj - drift_ask_adj}")
    elif drift_bid_adj > vertex_ask_adj:
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
