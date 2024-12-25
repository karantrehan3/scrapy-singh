from scrapy import Spider, Request
from scrapy.exceptions import CloseSpider
import json
import time
from src.cache import cache
from src.db import database


class ProductsSpider(Spider):
    name = "products"

    def __init__(self, base_url, num_pages, proxy=None, *args, **kwargs):
        """
        Initialize the ProductsSpider with the given parameters.
        """
        super().__init__(*args, **kwargs)
        self.base_url = base_url
        self.num_pages = int(num_pages)
        self.proxy = proxy
        self.start_urls = [f"{base_url}page/{i}/" for i in range(1, self.num_pages + 1)]
        self.custom_settings = {
            "USER_AGENT": "Mozilla/5.0",
            "HTTPPROXY_ENABLED": True,
            "DOWNLOAD_DELAY": 1,
            "CONCURRENT_REQUESTS": 4,
            "PROXY": self.proxy,
        }
        self.cache = cache
        self.database = database
        self.retry_attempts = 3

    def parse(self, response):
        """
        Parse the response from the product page.
        """
        products = self.cache.hgetall_values(self.name)

        for card in response.xpath("/html/body/div[1]/div[2]/div/div/div/div[4]/ul/li"):
            product = {
                "product_title": card.xpath(".//div[1]/a/img/@alt").get(),
                "product_price": card.xpath(
                    ".//div[2]/div[2]/span[1]/ins/span/bdi/text()"
                ).get(),
                "path_to_image": card.xpath(".//div[1]/a/img/@data-lazy-src").get(),
            }

            # Check cache to avoid updating unchanged products
            cached_data = self.cache.hget(self.name, product["product_title"])
            if cached_data:
                cached_product = json.loads(cached_data)
                if cached_product["product_price"] == product["product_price"]:
                    continue

            self.cache.hset(self.name, product["product_title"], product)
            products.append(product)

        self.database.save(products)

    def start_requests(self):
        """
        Generate the initial requests for the spider.
        """
        for url in self.start_urls:
            for attempt in range(self.retry_attempts):
                try:
                    yield Request(url, callback=self.parse, errback=self.errback)
                    break
                except CloseSpider:
                    if attempt < self.retry_attempts - 1:
                        time.sleep(2**attempt)
                    else:
                        raise

    def errback(self, failure):
        """
        Handle errors during requests.
        """
        self.logger.error(repr(failure))
