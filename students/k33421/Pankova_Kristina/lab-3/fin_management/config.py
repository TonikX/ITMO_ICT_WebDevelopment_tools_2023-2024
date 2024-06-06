from celery.schedules import crontab

# Настройки Celery
CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Настройки планирования задач
CELERY_BEAT_SCHEDULE = {
    'parse_url': {
        'task': 'tasks.parse_url',
        'schedule': crontab(minute='*/1'),
        'args': ('https://career.habr.com/vacancies?page=2&s%5B%5D=2&s%5B%5D=3&s%5B%5D=82&s%5B%5D=4&s%5B%5D=5&s%5B%5D=72&s%5B%5D=1&s%5B%5D=75&s%5B%5D=6&s%5B%5D=77&s%5B%5D=7&s%5B%5D=83&s%5B%5D=84&s%5B%5D=8&s%5B%5D=85&s%5B%5D=73&s%5B%5D=9&s%5B%5D=86&s%5B%5D=106&type=all',)
    }
}
