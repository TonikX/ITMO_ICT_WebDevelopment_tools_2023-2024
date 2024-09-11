import asyncio
import aiohttp
import time
import requests
from bs4 import BeautifulSoup
from sqlalchemy.dialects.postgresql import asyncpg

from students.K33391.Volgin_Leonid.Lab_2.task_2.conn import init_db, sion
from models import *
from urls import URLS


async def parse_and_save(url):
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(url) as response:
                r = await response.text()
                soup = BeautifulSoup(r, 'html.parser')
                print("Listening music from: ",soup.find('title').text)
                title = soup.find('title').text
                songs = soup.find_all('div', class_="name_track")
                for song in songs:
                    try:
                        author = song.find('span', class_='artist').get_text()
                        name = song.find('span', class_='song').get_text()
                        #postgresql://postgres:Scalapendra1219212712192127@localhost:5433/song_database
                        async with asyncpg.connect(
                                host='localhost',
                                port=5433,
                                user='postgres',
                                password='Scalapendra1219212712192127',
                                database='song_database'
                        ) as conn:

                            async with conn.cursor() as cur:
                                sql = "INSERT INTO song (title, author, name) VALUES (%s, %s, %s)"
                                data = [title, author, name]
                                await cur.execute(sql, data)
                                #await cur.execute("SELECT * FROM song")
                                #rows = await cur.fetchall()
                                #for row in rows:
                                #    print(row)


                        #print(author,': ', name)
                        #pesnya = Song(name=name, author=author, title=title)
                        #sion.add(pesnya)
                        #sion.commit()
                    except Exception as e:
                        pass
    except Exception as ex:
        pass

async def main():
    tasks = []
    for url in URLS:
        task = asyncio.create_task(parse_and_save(url))
        tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    init_db()
    start_time = time.time()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
    end_time = time.time()
    print(f"Async time ': {end_time - start_time} seconds")