import asyncio
import time
import config
import aiohttp
from bs4 import BeautifulSoup
from connection import DataBaseConnection


async def get_bio(session, url):
    async with session.get(url) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.find('div', class_='xZmPc')
        bio_container = text.find('div')
        if bio_container.em and bio_container.em.text:
            return bio_container.em.text
        if bio_container.text:
            return bio_container.text


async def parse_and_save(url, db_conn):
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                tasks = soup.find_all('div', class_='CHPy6')
                for task in tasks:
                    name = task.find('div', class_='dbENL').text + ' ' + task.find('div', class_='p1Gbz').text
                    bio = await get_bio(session, 'https://www.culture.ru' + task.a['href'])

                    with db_conn.cursor() as cursor:
                            cursor.execute(DataBaseConnection.INSERT_SQL, (name, bio))

                db_conn.commit()
    except Exception as e:
        print("Error:", e)
        
        
async def process_url_list(url_list, conn):
    tasks = []
    for url in url_list:
        task = asyncio.create_task(parse_and_save(url, conn))
        tasks.append(task)
    await asyncio.gather(*tasks)


async def main():
    urls = config.URLS
    num_threads = config.NUM_THREADS
    chunk_size = len(urls) // num_threads
    url_chunks = [urls[i:i + chunk_size] for i in range(0, len(urls), chunk_size)]
    db_conn = DataBaseConnection.connect_to_database()

    await asyncio.gather(*(process_url_list(chunk, db_conn) for chunk in url_chunks))

    db_conn.close()


if __name__ == '__main__':
    start_time = time.time()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")