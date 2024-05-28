# База сумматора
Для упрощения кода и эффективности воспользуемся реализацией скрапера на async/await. Так как нас не интересуют метрики скорости выполнения, то будем вызывать скрапер непосредственно из функции _calculate_async и уберем run из базового класса скрапера:
```Python
class AsyncScrape(BaseScraper):
    def __str__(self):
        return "AsyncScrape"

    async def _async_save(self, link):
        req = self.session.get("http:" + link, timeout=8)
        print(f"Fetching {link}...")
        if req.status_code == 200:
            img = req.content
            self.save_img(img)
        else:
            print(f"Status {req.status_code}")

    async def _async_parse(self, num):
        img_links = self.extract_img_urls(num)
        tasks = []
        for link in img_links:  # processing links
            task = asyncio.create_task(self._async_save(link))
            await task
            self.rows.append((self.base_url + "/" + f"{num}", link))
            print(f"Parsing {num}...")
            await asyncio.sleep(1.5)

    async def _calculate_async(self):
        tasks = []
        for i in self.page_range:
            task = asyncio.create_task(self._async_parse(i))
            tasks.append(task)
            await asyncio.sleep(3)

        await asyncio.gather(*tasks)
```
В класс BaseScraper добавим аттрибут self.rows, который будет хранить список данных добавляемых в БД:
```Python
class BaseScraper:
    _results = [] # хранит результаты времени выполнения
    """
    Базовый класс для скрейпера. В дальнейшем будет наследоваться
    у реализаций на asyncio, multiprocessing и threading
    """

    # передаем url с тегом и количество страниц для парсинга
    def __init__(self, base_url: str, start: int, end: int):
        self.rows = []
```
BackendHandler из второй лабораторной работы вызывает несколько проблем при работе с FastAPI. Первая - библиотека requests часто замораживает потоки (таймаут не помог), вторая - хардкодинг адреса для запроса к API, третья - использование запроса к API, а не API напрямую:
```Python
class BackendHandler:
    def __init__(self):
        self.url = "http://127.0.0.1:8000/"
        self.session = requests.session()

    def append_row(self, img_source, img_link):
        data = json.dumps({"url": img_source})
        imgsource_req = self.session.post(self.url + 'add_imgsource', data=data)
        if imgsource_req.status_code == 200:
            data = json.dumps({"url": img_link, "imagesource_id": imgsource_req.json()['id']})
            img_req = self.session.post(self.url + 'add_img', data=data)
            if img_req.status_code == 200:
                print('Added to backend')
            else:
                print(f"Image failed: {img_req.content}")
        else:
            print(f"Image source failed: {imgsource_req.content}")
```
Уберем его и заменим на что-то более умное в следующем разделе.
