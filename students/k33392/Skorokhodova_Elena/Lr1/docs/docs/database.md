#Подключение БД

Этот код создает несколько объектов SQLAlchemy для работы с базой данных.
Предварительно я скачала PostgreSQL и через pgAdmin создала БД, к которой потом
подключилась в приложении.

    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    
    SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:123123@localhost:3000/mydb"
    
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    Base = declarative_base()


