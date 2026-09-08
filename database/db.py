import sqlite3
from datetime import datetime

def save_price(db_path, name, url, price):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(
            "INSERT INTO price_history (product_name, product_url, price, checked_at) VALUES (?, ?, ?, ?)",
            (name, url, price, datetime.now().isoformat())
    )
    connection.commit()
    connection.close()

def get_last_price(db_path, url):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT price FROM price_history WHERE product_url = ? ORDER BY checked_at DESC LIMIT 1",
        (url,)
    )
    result = cursor.fetchone()
    connection.close()
    if result:
        return result[0]
    return None
    