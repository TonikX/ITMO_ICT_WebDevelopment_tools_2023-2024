from sqlmodel import create_engine, Session
from sqlalchemy.sql import text

class DataBaseConnection:
    INSERT_SQL = text("""INSERT INTO public.task(title, description, deadline, 
                                            created_date, priority, status, 
                                            category_id, user_id)
                    VALUES (:title, :description, :deadline, :created_date, 
                            :priority, :status, :category_id, :user_id)""")

    @staticmethod
    def connect_to_database():
        engine = create_engine(
            "postgresql://postgres:12345@postgres:5432/tasks_db"
        )
        return engine

    @staticmethod
    def insert_task(task_data):
        engine = DataBaseConnection.connect_to_database()
        with Session(engine) as session:
            session.execute(DataBaseConnection.INSERT_SQL, task_data)
            session.commit()