import asyncio
import aiohttp
from bs4 import BeautifulSoup
import asyncpg
import time

DATABASE_URL = "postgresql://postgres:23465@localhost/laboratory_work_2"

async def create_table_if_not_exists():
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS pages_1 (
                id SERIAL PRIMARY KEY,
                url TEXT NOT NULL,
                title TEXT NOT NULL
            )
        ''')
        print("Table 'pages' created or already exists.")
        await conn.close()
    except Exception as e:
        print(f"Error creating table: {e}")

async def parse_and_save(session, url):
    async with session.get(url) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string if soup.title else 'No title found'

        retries = 3
        for attempt in range(retries):
            try:
                conn = await asyncpg.connect(DATABASE_URL)
                await conn.execute(
                    "INSERT INTO pages_1 (url, title) VALUES ($1, $2)", url, title
                )
                await conn.close()
                print(f"Title of {url}: {title}")
                break
            except asyncpg.exceptions.UniqueViolationError:
                print(f"Entry for {url} already exists.")
                break
            except (asyncpg.exceptions.ConnectionDoesNotExistError, asyncpg.exceptions.InterfaceError) as e:
                if attempt < retries - 1:
                    print(f"Attempt {attempt + 1} failed, retrying... Error: {e}")
                    await asyncio.sleep(2)
                else:
                    print(f"Error saving data after {retries} attempts: {e}")
            except Exception as e:
                print(f"Error saving data: {e}")
                break 

async def main():
    urls = ["https://github.com/", "https://gitlab.com/", "https://www.youtube.com/"]

    await create_table_if_not_exists()

    async with aiohttp.ClientSession() as session:
        tasks = [parse_and_save(session, url) for url in urls]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Затраченное время: {execution_time}")
