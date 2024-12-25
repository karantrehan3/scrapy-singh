# scrapy-singh

## Overview

This project is a web scraping tool built using FastAPI and Scrapy. It scrapes product data from a specified website and stores the data in a JSON file. The project uses Redis for caching and Docker for containerization.

## Tech Stack

- **FastAPI**: A modern, fast (high-performance), web framework for building APIs.
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
│   ├── scraper/
│   │   └── products_spider.py
│   ├── app.py
│   ├── utils/
│   │   ├── cache.py
│   │   ├── db.py
│   │   └── notifier.py
│   ├── config/
│   │   └── __init__.py
├── .env
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Setup

1. **Clone the repository**:

   ```sh
   git clone https://github.com/karantrehan3/scrapy-singh.git
   cd scrapy-singh
   ```

2. **Create a [`.env`](.env) file**:
   Copy the [`.env.example`](.env.example) file to [`.env`](.env) and fill in the required environment variables.

   ```sh
   cp .env.example .env
   ```

3. **Build and start the Docker containers**:

   ```sh
   docker-compose up --build
   ```

4. **Access the FastAPI Docs**:
   The server will be running at port 8000 and docs will be available at `http://localhost:8000/docs`.

### API Endpoints

- **Health Check**: `GET /health`

  - Returns a simple message indicating the server is running.

  ```sh
  curl --location 'http://localhost:8000/health'
  ```

- **Scrape Products**: `POST /scrape`

  - Query Parameters:
    - `num_pages` (optional): Number of pages to scrape. Default is 1.
    - `retry_attempts` (optional): Number of retry attempts for failed requests. Default is 3.
    - `proxy` (optional): Proxy to use for scraping.
  - Starts the scraping process and saves the scraped data to a JSON file.

  ```sh
  curl --location --request POST 'http://localhost:8000/scrape?num_pages=&retry_attempts=&proxy=' \
  --header 'Authorization: your_static_token'
  ```

### Note: Multiple requests to POST /scrape in the same runtime do not work.

> I am aware about the one issue where more than one API call won't yield results but will give an error `twisted.internet.error.ReactorNotRestartable`. This is because scrapy starts a reactor when `process.start()` is called and this cannot be restarted. There are solutions for this out there but I have not been able to integrate one in the current scenario yet. Working on resolving this.

## How Scraping Works

1. **Scraping Process**:

   - The [`ProductsSpider`](src/scraper/products_spider.py) class in [`src/scraper/products_spider.py`](src/scraper/products_spider.py) is responsible for scraping product data.
   - It takes `base_url`, `num_pages`, `retry_attempts`, and `proxy` as parameters.
   - It fetches product details such as title, price, and image path from the specified pages.

2. **Caching**:

   - The [`Cache`](src/utils/cache.py) class in [`src/utils/cache.py`](src/utils/cache.py) uses Redis to cache scraped data.
   - It checks the cache to avoid updating unchanged products and caches the entire product list for later use.

3. **Database**:

   - The [`Database`](src/utils/db.py) class in [`src/utils/db.py`](src/utils/db.py) saves the scraped data to a JSON file.

4. **Notifier**:

   - The [`Notifier`](src/utils/notifier.py) class in [`src/utils/notifier.py`](src/utils/notifier.py) is responsible for notifying the user by logging the message to the console.

5. **Routes**:
   - The [`scrape`](src/routes/scrape.py) endpoint in [`src/routes/scrape.py`](src/routes/scrape.py) starts the scraping process and saves the data to the database.
   - The [`auth`](src/routes/auth.py) module in [`src/routes/auth.py`](src/routes/auth.py) handles API key authentication.

## Configuration

- **Environment Variables**:
  - `AUTH_TOKEN`: Authentication token for API requests.
  - `REDIS_HOST`: Redis server host.
  - `REDIS_PORT`: Redis server port.
  - `SERVER_PORT`: Port on which the FastAPI server runs.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
