from fastapi import APIRouter
from src.scraper.spiders.products_spider import ProductsSpider
from scrapy.crawler import CrawlerProcess
from src.db import Database
from src.cache import cache
import json

scrape_router = APIRouter()

database = Database()

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

    # Fetch cached data and write to JSON if updated
    cached_products = cache.get("scraped_products")
    if cached_products:
        scraped_data = json.loads(cached_products)
    else:
        scraped_data = []

    database.save(scraped_data)
    return {"message": f"Scraping complete. {len(scraped_data)} products saved."}
