import csv
from datetime import datetime

# Path to the CSV file
csv_file = 'arbitrage_opportunities.csv'

# Variables to store results
consecutive_opportunities_count = 0
cumulative_profit = 0.0

# Variables to track state across rows
previous_opportunity = None
is_consecutive = False

# Define loss percentage for isolated opportunities
loss_percentage = 0.0015  # 0.15%

# Convert timestamp strings to datetime objects for easier time comparison
def parse_timestamp(timestamp_str):
    return datetime.fromisoformat(timestamp_str)

with open(csv_file, mode='r') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        # Parse relevant fields from the current row
        profit_after_fees = float(row['profit_after_fees'])
        current_timestamp = parse_timestamp(row['timestamp'])
        buy_price = float(row['buy_price'])
        sell_price = float(row['sell_price'])
        
        if previous_opportunity:
            # Parse previous opportunity details
            prev_timestamp = parse_timestamp(previous_opportunity['timestamp'])
            prev_buy_price = float(previous_opportunity['buy_price'])
            prev_sell_price = float(previous_opportunity['sell_price'])

            # Check if the current opportunity is within 10 seconds of the previous one
            time_diff = (current_timestamp - prev_timestamp).total_seconds()
            same_price = (buy_price == prev_buy_price or sell_price == prev_sell_price)

            if time_diff <= 10 and same_price:
                # Count consecutive opportunity within 10 seconds if it's a "new" second tick
                if not is_consecutive:
                    consecutive_opportunities_count += 1
                    is_consecutive = True  # Mark as part of consecutive opportunities
                    # Accumulate profit starting from the second opportunity
                    cumulative_profit += profit_after_fees
                else:
                    # Continue accumulating profit for consecutive opportunities within the same window
                    cumulative_profit += profit_after_fees
            else:
                # Apply a 0.15% loss based on the buy price if the previous opportunity is isolated
                if not is_consecutive:
                    loss = prev_buy_price * loss_percentage
                    cumulative_profit -= loss
                    print(f"Isolated opportunity. Applied 0.15% loss based on buy price: -{loss:.2f}")
                is_consecutive = False

        # Update previous opportunity to the current row for the next iteration
        previous_opportunity = row

# Output the results
print(f"Number of consecutive arbitrage opportunities: {consecutive_opportunities_count}")
print(f"Accumulated profit with isolated opportunity losses applied: {cumulative_profit:.2f}")
