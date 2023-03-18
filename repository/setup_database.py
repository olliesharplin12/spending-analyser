import sqlite3


DATABASE_NAME = "spending.db"

def setup_database():
    conn = sqlite3.connect(DATABASE_NAME)

    # Create transactiosn table if it doesn't exist
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_type TEXT NOT NULL,
            details TEXT,
            particulars TEXT,
            code TEXT,
            reference TEXT,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            foreign_currency_amount REAL,
            conversion_charge REAL,
            title TEXT NOT NULL,
            category_id INTEGER
        )
    """)  # TODO: Category ID should be stored as string or reference Category table.

    # Commit changes and close connection
    conn.commit()
    conn.close()
