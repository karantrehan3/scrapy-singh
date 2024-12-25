# scrapy-singh

## Overview

This project is a web scraping tool built using FastAPI and Scrapy. It scrapes product data from a specified website and stores the data in a JSON file. The project uses Redis for caching and Docker for containerization.

## Tech Stack

- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- **Scrapy**: An open-source and collaborative web crawling framework for Python.
- **Redis**: An in-memory data structure store, used as a database, cache, and message broker.
- **Docker**: A set of platform-as-a-service products that use OS-level virtualization to deliver software in packages called containers.

## Project Structure

```
.
├── src/
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── scrape.py
│   ├── srcaper/
│   │   └── spiders/
│   │       └── product_spider.py
│   ├── app.py
│   ├── cache.py
│   ├── config.py
│   └── db.py
├── .env
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Setup

1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create a [`.env`](.env ) file**:
    Copy the [`.env.example`](.env.example ) file to [`.env`](.env ) and fill in the required environment variables.
    ```sh
    cp .env.example .env
    ```

3. **Build and start the Docker containers**:
    ```sh
    docker-compose up --build
    ```

4. **Access the FastAPI server**:
    The server will be running at `http://localhost:8000`.

### API Endpoints

- **Health Check**: `GET /health`
    - Returns a simple message indicating the server is running.

- **Scrape Products**: `GET /scrape`
    - Parameters:
        - [`num_pages`](src/scraper/spiders/products_spider.py ) (optional): Number of pages to scrape. Default is 1.
        - [`proxy`](src/scraper/spiders/products_spider.py ) (optional): Proxy to use for scraping.
    - Starts the scraping process and saves the scraped data to a JSON file.

## How Scraping Works

1. **Scraping Process**:
    - The [`ProductsSpider`](src/scraper/spiders/products_spider.py ) class in [`src/scraper/spiders/products_spider.py`](src/scraper/spiders/products_spider.py ) is responsible for scraping product data.
    - It takes [`base_url`](src/scraper/spiders/products_spider.py ), [`num_pages`](src/scraper/spiders/products_spider.py ), and [`proxy`](src/scraper/spiders/products_spider.py ) as parameters.
    - It fetches product details such as title, price, and image path from the specified pages.

2. **Caching**:
    - The [`Cache`](src/cache.py ) class in [`src/cache.py`](src/cache.py ) uses Redis to cache scraped data.
    - It checks the cache to avoid updating unchanged products and caches the entire product list for later use.

3. **Database**:
    - The [`Database`](src/db.py ) class in [`src/db.py`](src/db.py ) saves the scraped data to a JSON file ([`scraped_data.json`](src/routes/scrape.py )).

4. **Routes**:
    - The [`scrape`](src/routes/scrape.py ) endpoint in [`src/routes/scrape.py`](src/routes/scrape.py ) starts the scraping process and saves the data to the database.
    - The [`auth`](src/routes/auth.py ) module in [`src/routes/auth.py`](src/routes/auth.py ) handles API key authentication.

## Configuration

- **Environment Variables**:
    - [`AUTH_TOKEN`](src/config.py ): Authentication token for API requests.
    - [`REDIS_HOST`](src/config.py ): Redis server host.
    - [`REDIS_PORT`](src/config.py ): Redis server port.
    - [`SERVER_PORT`](src/config.py ): Port on which the FastAPI server runs.

## License

This project is licensed under the MIT License. See the LICENSE file for details.