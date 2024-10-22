import asyncio
import aiohttp
import psycopg2
from time import time


async def parse_url(url, session):
    async with session.get(url) as resp:
        with psycopg2.connect(host='localhost', database='hackathon_db', user='postgres', password=123, port=5432) as conn:
            with conn.cursor() as cur:
                conn.autocommit = True

                response = await resp.json()

                for post in response['posts']:
                    title = post['title']
                    descr = post['descr'].replace("<br />", "").replace("&nbsp;", " ")

                    try:
                        data = title, descr
                        cur.execute("INSERT INTO competition (name, description) VALUES ('%s', '%s')" % data)
                            
                    except Exception as e:
                        conn.rollback()
                        print(e)

                conn.rollback()

async def main():
    urls = ["https://feeds.tildacdn.com/api/getfeed/?feeduid=131632209651-986950497851",
        "https://feeds.tildacdn.com/api/getfeed/?feeduid=617755803461"]

    async with aiohttp.ClientSession() as session:
        tasks = [parse_url(url, session) for url in urls]
        await asyncio.gather(*tasks)


if __name__=="__main__":
    start_time = time()

    asyncio.run(main())

    end_time = time()
    print(end_time - start_time)