import os
import requests
from scrapy import Spider, Request
from scrapy.exceptions import CloseSpider
from scrapy.http import Response
from typing import List, Dict, Any, Generator
import time
from src.utils.cache import cache
from src.utils.db import database
from src.utils.notifier import Notifier


class ProductsSpider(Spider):
    name = "products"

    def __init__(
        self,
        base_url: str,
        num_pages: int,
        retry_attempts: int,
        proxy: str = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
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
        self.retry_attempts = retry_attempts

    def parse(self, response: Response) -> None:
        """
        Parse the response from the product page.
        """
        products: List[Dict[str, str]] = []
        for card in response.xpath("/html/body/div[1]/div[2]/div/div/div/div[4]/ul/li"):
            product_title = card.xpath(".//div[1]/a/img/@alt").get()

            price_element = card.xpath(".//div[2]/div[2]/span[1]")
            starting_at_price = price_element.xpath(
                ".//span[contains(@class, 'starting')]/following-sibling::span/bdi/text()"
            ).get()
            regular_price = price_element.xpath(".//ins/span/bdi/text()").get()
            product_price = (
                f"Starting at: ₹{starting_at_price}"
                if starting_at_price
                else f"₹{regular_price}"
            )

            image_url = card.xpath(".//div[1]/a/img/@data-lazy-src").get()

            product = {
                "product_title": product_title,
                "product_price": product_price,
                "product_image_url": image_url,
                "path_to_image": (
                    self.download_image(image_url, product_title) if image_url else None
                ),
            }

            # Check cache to avoid updating unchanged products
            cached_data = self.cache.hget(self.name, product["product_title"])
            if cached_data:
                if cached_data["product_price"] == product["product_price"]:
                    continue

            self.cache.hset(self.name, product["product_title"], product)
            products.append(product)

        updated_count, inserted_count = self.database.save(products, "product_title")
        Notifier.notify(f"Updated: {updated_count}, Inserted: {inserted_count}")

    def download_image(self, url: str, product_title: str) -> str:
        """
        Download the image from the given URL and save it to the storage/images directory.
        Return the absolute path to the saved image.
        """
        directory = "storage/images"
        os.makedirs(directory, exist_ok=True)
        sanitized_title = product_title.replace(" ", "_")
        file_path = os.path.join(directory, f"{sanitized_title}.jpg")

        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, "wb") as file:
                file.write(response.content)
            return os.path.abspath(file_path)
        else:
            return None

    def start_requests(self) -> Generator[Any, Any, Any]:
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

    def errback(self, failure: Any) -> None:
        """
        Handle errors during requests.
        """
        self.logger.error(repr(failure))
