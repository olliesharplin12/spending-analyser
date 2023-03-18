import csv
import os
import sys
from typing import List

from models.Transaction import Transaction
from models.Category import Category
from util.util import clear_terminal
from repository.setup_database import setup_database
from repository.transactions import insert_transactions, transaction_exists


CSV_PATH = os.path.join("exports", "01-0877-0215630-00_Transactions_2023-01-04_2023-03-18.csv")
CSV_HEADERS = ["Type", "Details", "Particulars", "Code", "Reference", "Amount", "Date", "ForeignCurrencyAmount", "ConversionCharge"]


def parse_csv_file(csv_file_path: str) -> List[Transaction]:
    transactions = []
    with open(csv_file_path, 'r') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        if len(CSV_HEADERS) != len(headers) or not all([header in CSV_HEADERS for header in headers]):
            print("CSV headers to not match expected values")
            sys.exit(1)

        for row in reader:
            transaction = Transaction(row[CSV_HEADERS[0]], row[CSV_HEADERS[1]], row[CSV_HEADERS[2]], row[CSV_HEADERS[3]], row[CSV_HEADERS[4]], row[CSV_HEADERS[5]], row[CSV_HEADERS[6]], row[CSV_HEADERS[7]], row[CSV_HEADERS[8]])
            transactions.append(transaction)

    return transactions

CATEGORY_LIST = [
    "Ignore", 
    "Food/Supermarket", 
    "Exercise", 
    "Subscription", 
    "Gaming", 
    "Outgoing", 
    "Alcohol", 
    "Clothing", 
    "Misc", 
    "Supplements", 
    "Holiday", 
    "Health", 
    "Appointments", 
    "Betting"
]

CATEGORIES = [Category(i+1, CATEGORY_LIST[i]) for i in range(len(CATEGORY_LIST))]

def print_categories():
    print("Spending Categories:")
    for i in range(len(CATEGORIES)):
        category = CATEGORIES[i]
        print(f"\t({i+1}) {category.name}")

# TODO: Add ability to transaction into multiple categories
def get_category_id(transaction: Transaction) -> int:
    print_categories()

    category_ids = [category.id for category in CATEGORIES]

    selected_category_id = None
    while selected_category_id is None:
        print()
        print("Select category for transaction:")
        print(f"\t[{transaction.date}] {transaction.transaction_type} - {transaction.title} ({transaction.amount})")
        print()

        try:
            user_input = int(input())
        except ValueError:
            user_input = None

        if user_input in category_ids:
            selected_category_id = user_input
        
        if selected_category_id is None:
            print("Invalid selection. Input the ID of a category listed above.")
    
    return selected_category_id

def main():
    # Setup database
    setup_database()

    # Parse CSV file into transaction instances
    transactions = parse_csv_file(CSV_PATH)

    # Filters transactions to expenses only and skips existing transactions
    expenses = []
    skipped_transactions = []
    for transaction in transactions:
        if not transaction.is_expense():
            continue

        if transaction_exists(transaction):
            skipped_transactions.append(transaction)
            continue

        expenses.append(transaction)

    if len(skipped_transactions) > 0:
        print("Transactions which already exist:")
        for transaction in skipped_transactions:
            print(f"\t{transaction}")

        print()
        user_input = input(f"Skipped {len(skipped_transactions)} transactions as they already exist.\nPress enter to proceed or type 'Q' to quit: ")
        if user_input.lower() == 'q':
            sys.exit(1)

    # Get and set category of each transaction
    for transaction in expenses:
        clear_terminal()
        category_id = get_category_id(transaction)
        transaction.set_category_id(category_id)
    
    # Write transaction details to database
    clear_terminal()
    ids = insert_transactions(expenses)

    if len(ids) != len(expenses):
        print("Error: Returned ids were not of same length as inserted transactions")
        sys.exit(1)

    for i in range(len(expenses)):
        expenses[i].set_id(ids[i])

    for transaction in expenses:
        print(transaction.id, transaction.title)


main()
