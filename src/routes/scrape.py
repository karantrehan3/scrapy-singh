from fastapi import APIRouter
from scrapy.crawler import CrawlerProcess
from scraper.products_spider import ProductsSpider
from src.utils.cache import cache
from src.utils.notifier import Notifier

scrape_router = APIRouter()


@scrape_router.get("/scrape")
async def scrape(num_pages: int = 1, proxy: str = None):
    process = CrawlerProcess()
    process.crawl(
        ProductsSpider,
        base_url="https://dentalstall.com/shop/",
        num_pages=num_pages,
        proxy=proxy,
    )
    process.start()

    # Fetch cached data if available else return empty list in the API response
    scraped_data = cache.hgetall_values(ProductsSpider.name)
    message = f"{'Balle Balle! Scraping complete.' if scraped_data else 'Scraping complete, par kuch mila nahi.'} {len(scraped_data)} products saved."

    Notifier.notify(message)
    return {
        "ok": True,
        "message": message,
        "data": scraped_data,
    }
