class BaseScraper:
    def __init__(self, driver):
        self.driver = driver

    def get_page(self, url):
        self.driver.get(url)

    def get_product_name(self):
        pass

    def get_product_price(self):
        pass