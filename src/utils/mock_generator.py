import csv
import random
import os
from datetime import date, timedelta

DESCRIPTIONS = [
    "Uber", "iFood", "Netflix", "Spotify", "Amazon", 
    "Supermarket", "Gas Station", "Pharmacy", "Gym", "Rent",
    "Internet Bill", "Electricity Bill", "Water Bill", "Restaurant"
]

def generate_mock_transactions(file_path: str, num_records: int = 1000) -> None:
    """
    Generates a CSV file with randomized and unsorted financial transactions.
    """
    start_date = date(2025, 1, 1)
    transactions = []

    for _ in range(num_records):
        random_days = random.randint(0, 365)
        tx_date = start_date + timedelta(days=random_days)
        
        tx_description = random.choice(DESCRIPTIONS)
        tx_amount = round(random.uniform(1.50, 1500.00), 2)
        
        transactions.append([tx_date.strftime("%Y-%m-%d"), tx_description, tx_amount])

    random.shuffle(transactions)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Description", "Amount"])
        writer.writerows(transactions)
        
    print(f"Successfully generated {num_records} records at '{file_path}'.")

if __name__ == "__main__":
    output_path = os.path.join("data", "transactions.csv")
    generate_mock_transactions(output_path)