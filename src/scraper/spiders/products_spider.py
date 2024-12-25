import scrapy
import json
from src.cache import cache


class ProductsSpider(scrapy.Spider):
    name = "products"

    def __init__(self, base_url, num_pages, proxy=None, *args, **kwargs):
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

    def parse(self, response):
        products = []
        cached_scraped_products = cache.get("scraped_products")
        if cached_scraped_products:
            products = json.loads(cached_scraped_products)

        for card in response.xpath("/html/body/div[1]/div[2]/div/div/div/div[4]/ul/li"):
            product = {
                "product_title": card.xpath(".//div[1]/a/img/@alt").get(),
                "product_price": card.xpath(
                    ".//div[2]/div[2]/span[1]/ins/span/bdi/text()"
                ).get(),
                "path_to_image": card.xpath(".//div[1]/a/img/@data-lazy-src").get(),
            }

            # Check cache to avoid updating unchanged products
            cached_data = cache.get(product["product_title"])
            if cached_data:
                cached_product = json.loads(cached_data)
                if cached_product["product_price"] == product["product_price"]:
                    continue

            cache.set(product["product_title"], json.dumps(product, indent=4))
            products.append(product)

        # Cache the entire product list for later use
        cache.set("scraped_products", json.dumps(products, indent=4))
        return products
