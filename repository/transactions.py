import sqlite3
from typing import List

from models.Transaction import Transaction
from .setup_database import DATABASE_NAME


def insert_transactions(transactions: List[Transaction]) -> List[int]:
    # Connect to database
    conn = sqlite3.connect(DATABASE_NAME)

    # Insert transactions into table
    inserted_ids = []
    for transaction in transactions:
        cursor = conn.execute('''
            INSERT INTO transactions (
                transaction_type,
                details,
                particulars,
                code,
                reference,
                amount,
                date,
                foreign_currency_amount,
                conversion_charge,
                title,
                category_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            transaction.transaction_type,
            transaction.details,
            transaction.particulars,
            transaction.code,
            transaction.reference,
            transaction.amount,
            transaction.date,
            transaction.foreign_currency_amount,
            transaction.conversion_charge,
            transaction.title,
            transaction.category_id
        ))

        inserted_ids.append(cursor.lastrowid)

    # Commit changes and close connection
    conn.commit()
    conn.close()

    return inserted_ids

def transaction_exists(transaction: Transaction) -> bool:
    # Connect to database
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Define the query
    query = '''
            SELECT * FROM transactions 
            WHERE transaction_type = ? AND details = ? AND particulars = ? AND code = ? 
            AND reference = ? AND amount = ? AND date = ? AND foreign_currency_amount = ? 
            AND conversion_charge = ?
            '''

    # Execute the query with the values of the transaction object
    cursor.execute(query, (transaction.transaction_type, transaction.details, transaction.particulars,
                        transaction.code, transaction.reference, transaction.amount,
                        transaction.date, transaction.foreign_currency_amount,
                        transaction.conversion_charge))

    # Get the results of the query
    results = cursor.fetchall()

    # Close connection
    conn.close()

    return len(results) > 0
