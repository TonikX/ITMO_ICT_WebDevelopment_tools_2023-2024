# Код ч.2 - asyncio

## asyncio

**Параллельный Парсинг**
С помощью ClientSession из aiohttp осуществляется асинхронный запрос к каждому URL. Для каждого URL выполняется функция parse_and_save, которая анализирует содержимое страницы и сохраняет извлеченные данные в базу данных.

```
async def fetch(url, session):
    async with session.get(url) as response:
        return await response.text()

async def parse_and_save(url, session):
    try:
        month_number = {
            "января": 1,
            "февраля": 2,
            "марта": 3,
            "апреля": 4,
            "мая": 5,
            "июня": 6,
            "июля": 7,
            "августа": 8,
            "сентября": 9,
            "октября": 10,
            "ноября": 11,
            "декабря": 12
        }
        content = await fetch(url, session)
        soup = BeautifulSoup(content, 'html.parser')

        title = soup.find('title').text.strip()
        
        description_meta = soup.find('meta', {'name': 'description'})
        description = description_meta['content'] if description_meta else ''
        
        value_span = soup.find('span', class_="Value-ie9gjh-2 iZlkBd")

        if value_span is not None:
            value_str = value_span.get_text().split()[0]
            value = float(value_str)

            if value > 8:
                priority = 1
            elif value > 6 and value < 8:
                priority = 2
            else:
                priority = 3
        else:
            priority = 4
        
 
        day_div = soup.find('div', class_='schedule-date__date')
        day = day_div.text.strip() if day_div else 'Пока неизвестно'


        month_div = soup.find('div', class_='schedule-date__month')
        month = month_div.text.strip().rstrip(';') if month_div else 'Пока неизвестно' 


        time_div = soup.find('div', class_='schedule-session')

        if time_div is not None:
            time = time_div.get_text().strip()
        else:
            time = 'Пока неизвестно'


        year = datetime.now().year  
        
        if day.lower() == "завтра":
            due_date = datetime.now() + timedelta(days=1)
        else:
            try:
                day_number = int(day)
                month_num = month_number.get(month.lower(), 1) 
                due_date = date(year, month_num, day_number)
            except ValueError:
                due_date = datetime.now()
        
        categories_names = [tag.text.strip() for tag in soup.select('.tags__item')]

        await save_to_db(title, description, priority, due_date, categories_names)

        print(f"Saved: {title} with priority {priority},  categories: {categories_names}, day: {day}, month: {month}, due_date {due_date},  time: {time}")
    except Exception as e:
        print(f"Error processing {url}: {e}")

async def save_to_db(title, description, priority, due_date, categories_names):
    async with async_session() as session:
        async with session.begin():
            task = Task(title=title, description=description, priority=priority, due_date=due_date)

            for category_name in categories_names:
                category = await session.get(Category, category_name)
                if not category:
                    category = Category(name=category_name)
                    session.add(category)
                    await session.commit()

                task.categories.append(category)

            session.add(task)
            await session.commit()

async def main():
    start_time = time.time() 
    
    urls = [
        "https://afisha.yandex.ru/saint-petersburg/standup/stand-up-kontsert-opytnykh-komikov-standuplabspb?city=saint-petersburg",
        "https://afisha.yandex.ru/saint-petersburg/standup/piterskii-stand-up?source=selection-events",
        "https://afisha.yandex.ru/saint-petersburg/standup/zhenskii-stendap-spletni?source=selection-events"
    ]

    async with ClientSession() as session:
        tasks = [parse_and_save(url, session) for url in urls]
        await asyncio.gather(*tasks)

    end_time = time.time()  
    total_time = end_time - start_time  
    print(f"Total execution time: {total_time} seconds")

if __name__ == '__main__':
    asyncio.run(main())

```