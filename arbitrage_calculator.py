# arbitrage_calculator.py
import csv
from datetime import datetime
import asyncio
from Vertex_Socket import vertex_data, start_vertex_socket
from drift_socket import drift_data, start_drift_socket


# Define CSV header and file path
csv_file = 'arbitrage_opportunities.csv'
csv_header = ["timestamp", "direction", "buy_price", "sell_price", "profit_after_fees", "spread", "time_gap_ms", "vertex_time", "drift_time"]

# Create CSV file and write the header if it doesn't already exist
try:
    with open(csv_file, mode='x', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_header)
except FileExistsError:
    pass  # File already exists, no need to write the header again

async def calculate_arbitrage():
    if vertex_data["bids"] is None or drift_data["bids"] is None:
        return

    # Get prices and times
    vertex_bid = vertex_data["bids"][0][0]
    vertex_ask = vertex_data["asks"][0][0]
    vertex_time = vertex_data["timestamp_ms"]
    vertex_time_ms = vertex_time / 1e6
    drift_bid = drift_data["bids"][0][0]
    drift_ask = drift_data["asks"][0][0]
    drift_time = drift_data["timestamp_ms"]


    #Debug
    print(f"Vertex - Ask: {vertex_ask}, Bid: {vertex_bid}, Time: {vertex_time_ms}")
    print(f"Drift - Ask: {drift_ask}, Bid: {drift_bid}, Time: {drift_time}")

    # Calculate time gap in milliseconds
    time_gap_ms = abs(vertex_time_ms - drift_time) / 1e6

    # Calculate adjusted bid/ask prices after fees
    vertex_fee_bps = 2
    drift_fee_bps = 2.125
    vertex_bid_adj = vertex_bid * (1 - vertex_fee_bps / 10000)
    vertex_ask_adj = vertex_ask * (1 + vertex_fee_bps / 10000)
    drift_bid_adj = drift_bid * (1 - drift_fee_bps / 10000)
    drift_ask_adj = drift_ask * (1 + drift_fee_bps / 10000)

    # Calculate potential profits for both directions
    profit_drift_to_vertex = vertex_bid_adj - drift_ask_adj  # Buy on Drift, sell on Vertex
    profit_vertex_to_drift = drift_bid_adj - vertex_ask_adj  # Buy on Vertex, sell on Drift

    # Track arbitrage opportunities in both directions
    opportunities = []

    if profit_drift_to_vertex > 0:
        opportunities.append({
            "direction": "Drift -> Vertex",
            "buy_price": drift_ask,
            "sell_price": vertex_bid,
            "profit_after_fees": profit_drift_to_vertex,
            "spread": vertex_bid - drift_ask,
            "time_gap_ms": time_gap_ms,
            "vertex_time": vertex_time,
            "drift_time": drift_time
        })
        print(f"Arbitrage opportunity (Drift -> Vertex): Buy on Drift at {drift_ask}, sell on Vertex at {vertex_bid}. "
              f"Profit after fees: {profit_drift_to_vertex}")

    if profit_vertex_to_drift > 0:
        opportunities.append({
            "direction": "Vertex -> Drift",
            "buy_price": vertex_ask,
            "sell_price": drift_bid,
            "profit_after_fees": profit_vertex_to_drift,
            "spread": drift_bid - vertex_ask,
            "time_gap_ms": time_gap_ms,
            "vertex_time": vertex_time,
            "drift_time": drift_time
        })
        print(f"Arbitrage opportunity (Vertex -> Drift): Buy on Vertex at {vertex_ask}, sell on Drift at {drift_bid}. "
              f"Profit after fees: {profit_vertex_to_drift}")
    #debug
    else:
        print("no arb")

    # Log opportunities to CSV
    if opportunities:
        timestamp = datetime.now().isoformat()
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            for opp in opportunities:
                writer.writerow([timestamp, opp["direction"], opp["buy_price"], opp["sell_price"], 
                                 opp["profit_after_fees"], opp["spread"], opp["time_gap_ms"], 
                                 opp["vertex_time"], opp["drift_time"]])

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
