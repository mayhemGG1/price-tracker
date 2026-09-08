import time
import logging

logger = logging.getLogger(__name__)

def retry(func, max_attempts=3, delay=5):
    for attempt in range(1, max_attempts+1):
        try:
            return func()
        except Exception as e:
            logger.warning(f"Спроба {attempt} невдала: {e}")
            if attempt < max_attempts:
                time.sleep(delay)
            else:
                raise


def clean_price(price_text):
    price_text = price_text.replace("₴", "")
    price_text = price_text.replace(" ", "")
    return int(price_text)