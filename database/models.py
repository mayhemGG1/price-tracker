import sqlite3


def create_table(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            product_url TEXT,
            price INTEGER,
            checked_at TEXT    
        )
    """)
    connection.commit()
    connection.close()