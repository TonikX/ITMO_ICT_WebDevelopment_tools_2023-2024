import asyncio
import datetime
from time import time

import aiohttp
import asyncpg
from bs4 import BeautifulSoup
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from models import Task

DATABASE_URL = "postgresql+asyncpg://postgres:Aliya2103@localhost:5432/todo"
engine = create_async_engine(DATABASE_URL, echo=True)
Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.text()


async def save_to_db(data):
    conn = await asyncpg.connect('postgresql://postgres:Aliya2103@localhost:5432/todo')
    try:
        for record in data:
            deadline = datetime.datetime.strptime(record['deadline'], '%Y-%m-%d').date() if record['deadline'] else None
            await conn.execute(
                "INSERT INTO task (title, description, deadline) VALUES ($1, $2, $3)",
                record['title'], record['description'], deadline
            )
    finally:
        await conn.close()
    return data  # Возвращаем сохраненные данные

async def dict_to_sentence(dictionary):
    sentence_words = [''] * (max(max(indices) for indices in dictionary.values()) + 1)
    for word, indices in dictionary.items():
        for index in indices:
            sentence_words[index] = word
    return ' '.join(sentence_words)

async def parse_and_save(url):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url) as response:
            page_with_results = await response.json()
            all_data = []
            if 'results' in page_with_results:
                for result in page_with_results['results']:
                    primary_topic = result.get('primary_topic')
                    if primary_topic:
                        domain_display_name = primary_topic.get('domain', {}).get('display_name', '')
                    else:
                        domain_display_name = ''
                    if domain_display_name:
                        title = result.get('title')
                        if title:
                            record = {'title': domain_display_name,
                                      'deadline': result.get('publication_date', '')}
                            for key, value in result.items():
                                if key not in ['id', 'title', 'publication_date']:
                                    record[key] = value
                            if 'abstract_inverted_index' in result and result['abstract_inverted_index']:
                                record['description'] = await dict_to_sentence(result['abstract_inverted_index'])
                                all_data.append(record)
            saved_data = await save_to_db(all_data)
            return saved_data

async def parse_and_save_to_db(start_page: int, end_page: int):
    urls = [f'https://api.openalex.org/works?page={i}&per-page=200' for i in range(start_page, end_page + 1)]
    tasks = [parse_and_save(url) for url in urls]
    results = await asyncio.gather(*tasks)
    all_results = [item for sublist in results for item in sublist]
    return all_results  # Возвращаем все сохраненные данные
