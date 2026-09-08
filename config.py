from dotenv import load_dotenv
import os

load_dotenv()


DB_PATH = "price_tracker.db"
PRICE_THRESHOLD = 8000

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")