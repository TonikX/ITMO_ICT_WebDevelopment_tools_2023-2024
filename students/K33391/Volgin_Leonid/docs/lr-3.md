# Практическое задание 1.3

Реализовать в своем проекте все улучшения, описанные в практике
Разобраться как передать в alembic.ini URL базы данных с помощью.env-файла и реализовать подобную передачу.

## Ход выполнения работы

### connection.py:
    import os
    from dotenv import load_dotenv
    from sqlmodel import SQLModel, Session, create_engine
    
    load_dotenv()
    db_url = os.getenv('DB_ADMIN')
    engine = create_engine(db_url, echo=True)

    def init_db():
        SQLModel.metadata.create_all(engine)

    def get_session():
        with Session(engine) as session:
            yield session


### env.py:
    ...
    import os

    load_dotenv()
    db_url = os.getenv("DB_URL")
    config = context.config
    config.set_main_option("sqlalchemy.url", db_url)
    target_metadata = SQLModel.metadata
    ...