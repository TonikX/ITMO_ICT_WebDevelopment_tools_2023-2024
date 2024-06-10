# БД
## Подключение к базе дынных

Было реализована подключение к рабочей базе данныз для хранения информации о пользователях и задачах:

    from sqlmodel import SQLModel, Session, create_engine
    
    db_url = 'postgresql://postgres:12345@localhost:5433/tasks_db'
    engine = create_engine(db_url, echo=True)
    
    
    def init_db():
        SQLModel.metadata.create_all(engine)
    
    
    def get_session():
        with Session(engine) as session:
            yield session
