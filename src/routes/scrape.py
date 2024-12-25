from fastapi import APIRouter, Query
from pydantic import BaseModel
from scrapy.crawler import CrawlerProcess
from scraper.products_spider import ProductsSpider
from src.utils.cache import cache
from src.utils.notifier import Notifier
from typing import Optional

scrape_router = APIRouter()


class ScrapeResponse(BaseModel):
    ok: bool
    message: str
    data: list[dict[str, str]]


@scrape_router.post(
    "/scrape",
    summary="Scrape Products",
    description="Scrape dental products from the website and return the scraped data.",
    response_model=ScrapeResponse,
    responses={
        200: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": {
                        "ok": True,
                        "message": "Balle Balle! Scraping complete. 2 products saved.",
                        "data": [
                            {"product_title": "Product 1", "product_price": "₹10.00"},
                            {
                                "product_title": "Product 2",
                                "product_price": "Starting at: ₹20.00",
                            },
                        ],
                    }
                }
            },
        },
    },
)
async def scrape(
    num_pages: int = Query(1, description="Number of pages to scrape"),
    retry_attempts: int = Query(
        3, description="Number of retry attempts in case of failure"
    ),
    proxy: Optional[str] = Query(None, description="Proxy server to use for scraping"),
) -> ScrapeResponse:
    process = CrawlerProcess()
    process.crawl(
        ProductsSpider,
        base_url="https://dentalstall.com/shop/",
        num_pages=num_pages,
        proxy=proxy,
        retry_attempts=retry_attempts,
    )
    process.start()

    # Fetch cached data if available else return empty list in the API response
    scraped_data = cache.hgetall_values(ProductsSpider.name)
    message = f"{'Balle Balle! Scraping complete.' if scraped_data else 'Scraping complete, par kuch mila nahi.'} {len(scraped_data)} products saved."

    Notifier.notify(message)
    return ScrapeResponse(
        ok=True,
        message=message,
        data=scraped_data,
    )
