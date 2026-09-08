from selenium.webdriver.common.by import By
from scrapers.base_scraper import BaseScraper
from utils import clean_price


class RozetkaScraper(BaseScraper):
    def get_product_name(self):
        name = self.driver.find_element(By.CSS_SELECTOR, "h1.d-inline")
        return name.text

    def get_product_price(self):
        price = self.driver.find_element(By.CSS_SELECTOR, "p.product-price__big")
        return clean_price(price.text)