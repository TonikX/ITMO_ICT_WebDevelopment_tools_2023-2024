import asyncio
import aiohttp
import sqlite3

urls = ["https://novabiom.ru/", "https://translate.google.com/?hl=ru&sl=tr&tl=ru&text=%C3%A7ok%20fazla%20spor&op=translate", "https://www.apple.com/"]

async def parse_and_save(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                html = await response.text()
                title = html.split('<title>')[1].split('</title>')[0]
                conn = sqlite3.connect('example.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO pages (url, title) VALUES (?, ?)", (url, title))
                conn.commit()
                conn.close()
                print("Page title saved:", title)

async def main():
    tasks = [parse_and_save(url) for url in urls]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
