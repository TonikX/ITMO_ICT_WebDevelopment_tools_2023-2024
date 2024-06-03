## Конфиг

    from celery import Celery
    
    celery_app = Celery("parser", broker='redis://redis:6379', backend='redis://redis:6379')
    
    celery_app.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json'
    )
    
    celery_app.autodiscover_tasks(['main'])

# Запрос в парсер

    parser_url = "http://parser:8081/parse"
    
    router = APIRouter(prefix="/parser", tags=["Parser"])
    
    
    @router.get("", response_model=dict)
    def parse(url: str):
        return requests.post(parser_url, params={'url': url}).json()

 