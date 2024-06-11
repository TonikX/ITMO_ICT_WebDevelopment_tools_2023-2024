import aiohttp
import asyncio
import asyncpg
import psycopg2
from time import time

def create_aiohttp_session():
    return aiohttp.ClientSession()


async def save_to_db(data):
    conn = await asyncpg.connect('postgresql://postgres:Aliya2103@localhost:5432/openalex_db')
    try:
        for record in data:
            await conn.execute(
                "INSERT INTO openalex_data (id, title, abstract, domain) VALUES ($1, $2, $3, $4)",
                record['id'], record['title'], record['abstract'], record['domain']
            )
    finally:
        await conn.close()

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
                            record = {'id': result['id'].replace("https://openalex.org/", ""),
                                      'domain': domain_display_name}
                            for key, value in result.items():
                                if key != 'id':
                                    record[key] = value
                            if 'abstract_inverted_index' in record and record['abstract_inverted_index']:
                                record['abstract'] = await dict_to_sentence(record['abstract_inverted_index'])
                                all_data.append(record)
            await save_to_db(all_data)

async def main_async():
    start_time = time()
    urls = [f'https://api.openalex.org/works?page={i}&per-page=200' for i in range(20, 26)]
    tasks = [parse_and_save(url) for url in urls]
    await asyncio.gather(*tasks)
    print(f"Time taken (async): {time() - start_time} seconds")

if __name__ == "__main__":
    asyncio.run(main_async())
