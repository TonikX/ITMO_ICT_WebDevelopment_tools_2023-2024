import asyncio
import aiohttp
import asyncpg
import time
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup

"""A script for fetching headers from URL and storing them in the database.
Uses asycnhronous approach.
"""

async def fetch_html(session, url):
    """A function for fetching html from provided URL.

Args:
    session: requests.Session object
    url: URL string

Returns:
    HTML as plain text or None if an error has occured.

Raises:
    Exception: An error occurred while decoding text for <URL>
    Exception: Request to <URL> failed with status code <status code>
    Exception: An error occurred while fetching html from <URL>
"""
    try:
        async with session.get(url) as response:
            if response.status == 200:
                try:
                    text = await response.text()
                    return text
                except Exception as e:
                    print(f"An error occurred while decoding text for {url}: {e}")
                    return None
            else:
                print(f"Request to {url} failed with status code {response.status}")
                return None
    except Exception as e:
        print(f"An error occurred while fetching html from {url}: {e}")
        return None


def extract_headers(html):
    """A function for extracting the headers section of html page.

Args:
    html: a string containing HTML page

Returns:
    HTML as plain text or None if an error has occured

Raises:
    Exception: An error occurred while extracting headers
"""
    try:
        soup = BeautifulSoup(html, "html.parser")
        head = soup.head
        return str(head) if head else None
    except Exception as e:
        print(f"An error occurred while extracting headers: {e}")
        return None


async def store_headers(url, headers):
    """A function for storing headers in the database.

Args:
    url: URL string
    headers: string containing the headers section

Raises:
    Exception: An error occurred while storing headers for <URL>
"""
    try:
        conn = await asyncpg.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME1"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        await conn.execute(
            "INSERT INTO html_headers (url, header_content) VALUES ($1, $2)",
            url, headers
        )
        await conn.close()
    except Exception as e:
        print(f"An error occurred while storing headers for {url}: {e}")


async def parse_and_save(session, url):
    """The task function for fetching html and storing it in the database.

Args:
    session: requests.Session object
    url: URL string
"""
    html = await fetch_html(session, url)
    if html is None:
        return
    headers = extract_headers(html)
    if headers is None:
        return
    await store_headers(url, headers)
    print(f"Headers for {url}:\n{headers}\n\n\n\n\n")


async def main():
    """The main function.
"""
    urls = ["https://example.com", "https://www.gnu.org", "https://www.wikipedia.org", "https://toscrape.com"]
    load_dotenv()

    async with aiohttp.ClientSession() as session:
        tasks = [parse_and_save(session, url) for url in urls]
        await asyncio.gather(*tasks)

    
if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    finish = time.time()    
    print(f"Time: {finish - start}")
