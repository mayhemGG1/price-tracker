import undetected_chromedriver as uc 
from scrapers.rozetka_scraper import RozetkaScraper
from database.models import create_table
from database.db import save_price, get_last_price
from config import DB_PATH, PRICE_THRESHOLD, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from notifications.telegram_notifier import send_message
from selenium.common.exceptions import NoSuchElementException
import logging
from utils import retry
import time
import schedule

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("price_tracker.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

create_table(DB_PATH)

url = "https://auto.rozetka.com.ua/ua/motoshlemi-kappa-150903405/p545649501/"

def check_price():
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = uc.Chrome(
        options=options,
        browse_executable_path="/usr/bin/chromium",
        driver_executable_path="/usr/bin/chromedriver",
        version_main=152
    )
    scraper = RozetkaScraper(driver)

    try:

        retry(lambda: scraper.get_page(url))
        driver.save_screenshot("/app/debug.png")

        name = scraper.get_product_name()
        price = scraper.get_product_price()


        last_price = get_last_price(DB_PATH, url)

        save_price(DB_PATH, name, url, price)
        logger.info(name)

        if last_price is None:
            logger.info(f"Перша перевірка. Поточна ціна: {price}")
        else:
            comparison = last_price - price
            logger.info(f"Ціна змінилась на: {comparison}")

        if price <= PRICE_THRESHOLD:
            message = f"Ціна на товар {name} впала нижче порогу!\nПоточна ціна: {price}\n Посилання: {url}"
            send_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)
        else:
            logger.info(f"Ціна поки що вища порогу. Поточна ціна: {price}")

    except NoSuchElementException:
        logger.error(f"Не вдалося знайти елемент на сторінці: {url}")
    except Exception as e:
        logger.error(f"Сталась невідома помилка: {e}")

    finally:
        driver.quit()

schedule.every().day.at("12:00").do(check_price)

while True:
    schedule.run_pending()
    time.sleep(60)
