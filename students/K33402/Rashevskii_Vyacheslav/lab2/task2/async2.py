import asyncio
import time
import aiohttp
from bs4 import BeautifulSoup
from connection import DB
from urls import URLs


async def parse_and_save_async(url, con):
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(url) as response:
                page = await response.text()
                soup = BeautifulSoup(page, 'html.parser')
                print(soup.find('title').text)  # сохранять заголовок страницы в базу данных по мне бесполезно
                # т.к. нагрузки 0 полезной, поэтому вывожу в консоль
                prs = soup.find_all('div',
                                    class_='Box-row Box-row--focus-gray p-0 mt-0 js-navigation-item js-issue-row')
                for pr in prs:
                    title = (pr.find('a',
                                     class_='Link--primary v-align-middle no-underline h4 js-navigation-open markdown-title').
                             text)
                    span_text = pr.find('span', class_='opened-by').text.split()
                    date = span_text[2] + ' ' + span_text[3][:-1] + ' ' + span_text[4]
                    author = span_text[6]
                    with con.cursor() as cursor:
                        cursor.execute(DB.INSERT_SQL, (title, date, author))

                con.commit()
    except Exception as e:
        print("Exception caught: ", e)


async def process_url_list_async(url_list, con):
    tasks = []
    for url in url_list:
        task = asyncio.create_task(parse_and_save_async(url, con))
        tasks.append(task)
    await asyncio.gather(*tasks)


async def main():
    count_for_1_thread = 2
    urls_for_1_thread = [URLs[i:i + count_for_1_thread] for i in range(0, len(URLs), count_for_1_thread)]

    con = DB.connect()

    await asyncio.gather(*(process_url_list_async(urls, con) for urls in urls_for_1_thread))

    con.close()


if __name__ == '__main__':
    start_time = time.time()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
    end_time = time.time()
    print(f"Time of execution 'async': {end_time - start_time} seconds")
