import asyncio
import datetime
import json
import time

import aiohttp
from bs4 import BeautifulSoup
from sqlalchemy.ext.asyncio import AsyncSession

import sys
import os
sys.path.append(os.path.expanduser('~/Desktop/ITMO_ICT_WebDevelopment_tools_2023-2024/students/k33421/aleksei_bezgin/lab1/hack_lab/app/db'))
sys.path.append(os.path.expanduser('~/Desktop/ITMO_ICT_WebDevelopment_tools_2023-2024/students/k33421/aleksei_bezgin/lab1/hack_lab/app'))

from connection import async_engine
from models import Hackathon, Task


async def add_hackathon(hack_info):
    hack_name, hack_link = hack_info['name'], hack_info['link']
    async with aiohttp.ClientSession() as session:
        async with session.get(hack_link) as response:
            inner_page = await response.text()
            soup_in = BeautifulSoup(inner_page, 'html.parser')
            paragraphs = [p.text for p in soup_in.find_all('p')]
            hack_case = '\n'.join(paragraphs)
            case_title = paragraphs[0]

    async with AsyncSession(async_engine) as session:
        hackathon = Hackathon(
            name=hack_name,
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now() + datetime.timedelta(days=7)
        )

        session.add(hackathon)
        await session.commit()
        await session.refresh(hackathon)

        task = Task(
            title=case_title,
            description=hack_case,
            requirements="Be cool",
            evaluation_criteria="Accuracy",
            hackathon_id=hackathon.id
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)


async def add_hackathon_list(hack_info_list):
    tasks = [add_hackathon(hack_info) for hack_info in hack_info_list]
    await asyncio.gather(*tasks)


async def main():
    hack_data = json.load(open('hack_links.json'))

    num_threads = 5
    step = len(hack_data) // num_threads

    time_start = time.time()
    tasks = []
    for i in range(num_threads):
        task = add_hackathon_list(hack_data[i * step: (i + 1) * step])
        tasks.append(task)

    await asyncio.gather(*tasks)

    print(f'scraped info about {len(hack_data)} events')
    print(f'done in {time.time() - time_start} seconds')


if __name__ == "__main__":
    asyncio.run(main())
