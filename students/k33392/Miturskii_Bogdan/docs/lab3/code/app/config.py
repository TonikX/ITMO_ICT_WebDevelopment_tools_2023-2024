class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://user:password@localhost/mydatabase"
    CELERY_BROKER_URL = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND = "redis://redis:6379/0"
