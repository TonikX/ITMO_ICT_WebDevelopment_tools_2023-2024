#Экземпляр Celery

Код настройки и создания экземпляра Celery для использования Redis в качестве брокера сообщений и хранилища результатов


    from celery import Celery
    
    app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')
    
    app.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='Europe/Moscow',
        enable_utc=True,
    )


###Задачи
Код создает задачу Celery, которая извлекает заголовок HTML-страницы по заданному URL. 
    
    from celery import Celery
    import requests
    from bs4 import BeautifulSoup
    
    app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')
    
    @app.task
    def parse_url(url: str):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else "No title found"
            return {"url": url, "title": title}
        except requests.RequestException as e:
            return {"error": str(e)}
