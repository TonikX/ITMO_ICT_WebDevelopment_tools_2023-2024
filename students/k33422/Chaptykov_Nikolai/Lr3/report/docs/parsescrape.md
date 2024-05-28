# Реализации скрапера/парсера
Напишем реализацию скрапера/парсера на потоках:
```Python
class ThreadScrape(BaseScraper):
    def __str__(self):
        return "ThreadScrape"

    def _thread_save(self, link):
        with self.session.get("http:" + link, timeout=8) as req:
            super().fetch(link)
            if req.status_code == 200:
                img = req.content
                self.save_img(img)
            else:
                print(f"Status {req.status_code}")

    def _thread_parse(self, num):
        img_links = self.extract_img_urls(num)
        with concurrent.futures.ThreadPoolExecutor(max_workers=NUMBER_OF_WORKERS) as executor:  # лимитируем потоки
            for link in img_links:  # обрабатываем ссылки
                super().parse(num)
                executor.submit(self._thread_save, link)
                print("Preparing to fire append row...")
                backend.append_row(self.base_url + "/" + f"{num}", link)
                time.sleep(1.5)

    def _calculate(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=NUMBER_OF_WORKERS) as executor:  # лимитируем потоки
            for i in self.page_range:
                executor.submit(self._thread_parse, i)
                time.sleep(5)
```
Напишем реализацию скрапера/парсера на asyncio:
```Python
class AsyncScrape(BaseScraper):
    def __str__(self):
        return "AsyncScrape"

    async def _async_save(self, link):
        with self.session.get("http:" + link, timeout=8) as req:
            print(f"Fetching {link}...")
            if req.status_code == 200:
                img = req.content
                self.save_img(img)
            else:
                print(f"Status {req.status_code}")

    async def _async_parse(self, num):
        img_links = self.extract_img_urls(num)
        tasks = []
        for link in img_links:  # обрабатываем ссылки
            task = asyncio.create_task(self._async_save(link))
            await task
            backend.append_row(self.base_url + "/" + f"{num}", link)
            print(f"Parsing {num}...")
            time.sleep(1.5)

    async def _calculate_async(self):
        tasks = []
        for i in self.page_range:
            task = asyncio.create_task(self._async_parse(i))
            tasks.append(task)
            time.sleep(5)

        await asyncio.gather(*tasks)

    def _calculate(self):
        asyncio.run(self._calculate_async())
```
Напишем реализацию скрапера/парсера на процессах:
```Python
class ProcessScrape(BaseScraper):
    def __str__(self):
        return "ProcessScrape"

    def _process_save(self, link):
        with self.session.get("http:" + link, timeout=8) as req:
            if req.status_code == 200:
                img = req.content
                self.save_img(img)
            else:
                print(f"Status {req.status_code}")

    def _process_parse(self, num):
        img_links = self.extract_img_urls(num)
        processes = []
        for link in img_links:  # обрабатываем ссылки
            p = Process(target=self._process_save, args=(link,))
            p.start()
            processes.append(p)
            backend.append_row(self.base_url + "/" + f"{num}", link)
            time.sleep(1.5)

        for p in processes:
            p.join()

    def _calculate(self):
        processes = []
        for i in self.page_range:
            p = Process(target=self._process_parse, args=(i,))
            p.start()
            processes.append(p)
            time.sleep(5)

        for p in processes:
            p.join()
```
Каждая из реализаций переключается между страницами с периодом 5 секунд и сохраняет картинки с каждой страницы с переиодом 1.5 секунд. На каждой странице находится около 12 изображений. Такой подход с задержкой позволяет избежать подозрений в DDoS-е