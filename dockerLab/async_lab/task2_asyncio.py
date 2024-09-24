import asyncio
from async_handlers import (
    parse_all_urls,
    data_handlers
)


async def parse_and_save():
    tasks = []
    for category, handler_func in data_handlers.items():
        url = f"https://async-lab.tiiny.site/{category}"
        print(url)
        tasks.append(parse_all_urls(handler_func, url, 5))

    # Запуск всех задач асинхронно
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    import time

    start_time = time.time()
    asyncio.run(parse_and_save())
    print("Execution time:", time.time() - start_time)
