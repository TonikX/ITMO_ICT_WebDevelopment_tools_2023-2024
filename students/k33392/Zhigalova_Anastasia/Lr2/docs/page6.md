# Код ч.2 - threading

## threading

**Многопоточность**
Thread из модуля threading. Использование многопоточности позволяет параллельно обрабатывать несколько URL, что ускоряет процесс сбора данных. Каждый поток выполняет функцию parse_and_save для отдельного URL.


```
def parse_and_save(url):
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
        response = requests.get(url)
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')

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

        title = soup.find('title').text.strip()
        
        description_meta = soup.find('meta', {'name': 'description'})
        description = description_meta['content'] if description_meta else ''

        categories_names = [tag.text.strip() for tag in soup.select('.tags__item')]

        
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
            
        save_to_db(title, description, priority, due_date, categories_names)

        print(f"Saved: {title} with priority {priority},  categories: {categories_names}, day: {day}, month: {month}, due_date {due_date},  time: {time}")
    except Exception as e:
        print(f"Error processing {url}: {e}")


def save_to_db(title, description, priority, due_date, categories_names):
    with Session(engine) as session:
        task = Task(title=title, description=description, priority=priority, due_date=due_date)

        for category_name in categories_names:
            category = session.query(Category).filter_by(name=category_name).first()
            if not category:
                category = Category(name=category_name)
                session.add(category)
                session.commit()

            task.categories.append(category)

        session.add(task)
        session.commit()

def main():

    start_time = time.time() 


    urls = [
        "https://afisha.yandex.ru/saint-petersburg/standup/stand-up-kontsert-opytnykh-komikov-standuplabspb?city=saint-petersburg",
        "https://afisha.yandex.ru/saint-petersburg/standup/piterskii-stand-up?source=selection-events",
        "https://afisha.yandex.ru/saint-petersburg/standup/zhenskii-stendap-spletni?source=selection-events"
        
    ]

    threads = []
    for url in urls:
        thread = Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()  
    total_time = end_time - start_time  
    print(f"Total execution time: {total_time} seconds")

if __name__ == '__main__':
    main()


```