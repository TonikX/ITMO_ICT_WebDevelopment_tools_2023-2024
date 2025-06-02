import asyncio
import aiohttp
import aiosqlite
import time

URLS = [
    "https://httpbin.org",
    "https://www.python.org",
    "https://habr.com",
    "https://github.com",
    "https://github.com",
    "https://github.com",
    "https://github.com",
    "https://github.com",
    "https://github.com",
    "https://github.com",
    "https://github.com",
    "https://github.com",
    "https://github.com",
    "https://github.com",
    "https://github.com",
]

async def fetch_title(session: aiohttp.ClientSession, url: str) -> tuple:
    try:
        async with session.get(url) as response:
            html = await response.text()
    except Exception as e:
        print(f"[Async] Failed to fetch {url}: {e}")
        return (url, "ERROR")
    title = "N/A"
    start = html.find("<title>")
    end = html.find("</title>")
    if start != -1 and end != -1:
        title = html[start+ len("<title>") : end].strip()
    print(f"[Async] Fetched title for {url}")
    return (url, title)

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_title(session, url) for url in URLS]
        results = await asyncio.gather(*tasks)
    async with aiosqlite.connect("pages.db") as db:
        await db.execute("CREATE TABLE IF NOT EXISTS pages (url TEXT, title TEXT)")
        await db.executemany("INSERT INTO pages (url, title) VALUES (?, ?)", results)
        await db.commit()
    return len(results)

if __name__ == "__main__":
    start_time = time.time()
    count = asyncio.run(main())
    elapsed = time.time() - start_time
    print(f"Saved {count} records to SQLite.")
    print(f"Completed in {elapsed:.2f} seconds")
