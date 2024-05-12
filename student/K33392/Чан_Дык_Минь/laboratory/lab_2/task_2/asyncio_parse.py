import asyncio
import time
from db import init_db, create_trip, TripDefault
from typing import List
from datetime import datetime, date
from bs4 import BeautifulSoup  # type: ignore
import aiohttp # type: ignore
from urls import URLS

async def fetch_content(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def parse_trip(url: str) -> TripDefault:
    content = await fetch_content(url)
    soup = BeautifulSoup(content, 'html.parser')
    title = soup.title.string
    date_start = date.today()
    date_end = date.today()
    estimated_cost = soup.find(lambda tag: tag.has_attr('class') and 'price' in tag['class'])
    if estimated_cost:
        estimated_cost = estimated_cost.text.strip()
        estimated_cost = float(''.join(filter(lambda x: x.isdigit() or x == '.', estimated_cost)))
    else:
        estimated_cost = 10000.0

    trip_status = "Asyncio"
    other_details = "The link to the trip is: " + url
    
    return TripDefault(
        title=title, 
        date_start=date_start, 
        date_end=date_end, 
        estimated_cost=estimated_cost, 
        trip_status=trip_status, 
        other_details=other_details
        )

async def save_trips(urls: List[str]):
    for url in urls:
        trip = await parse_trip(url)
        create_trip(trip)
        print(f"Trip saved: {trip}")

async def main():
    tasks = []

    for url in URLS:
        task = asyncio.create_task(save_trips(url))
        tasks.append(task)
    
    # Звездочка * перед tasks —  распаковывает список
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    init_db()
    start_time = time.time()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
    print(f"Execution time using Asyncio: {time.time() - start_time}")
