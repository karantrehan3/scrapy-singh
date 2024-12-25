from fastapi import APIRouter
from scrapy.crawler import CrawlerProcess
import json
from src.scraper.spiders.products_spider import ProductsSpider
from src.cache import cache

scrape_router = APIRouter()


@scrape_router.get("/scrape")
def scrape(num_pages: int = 1, proxy: str = None):
    process = CrawlerProcess()
    process.crawl(
        ProductsSpider,
        base_url="https://dentalstall.com/shop/",
        num_pages=num_pages,
        proxy=proxy,
    )
    process.start()

    # Fetch cached data if available else return empty list in the API response
    cached_products = cache.get("scraped_products")
    if cached_products:
        scraped_data = json.loads(cached_products)
    else:
        scraped_data = []

    return {
        "ok": True,
        "message": f"Scraping complete. {len(scraped_data)} products saved.",
        "scraped_data": scraped_data,
    }
