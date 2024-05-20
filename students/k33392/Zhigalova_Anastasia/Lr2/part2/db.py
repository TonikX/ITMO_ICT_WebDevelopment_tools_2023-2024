from requests import Session
from sqlalchemy import DateTime, Table, Column, Integer, ForeignKey, String, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

task_category_association = Table('task_category', Base.metadata,
    Column('task_id', Integer, ForeignKey('task.id')),
    Column('category_id', Integer, ForeignKey('category.id'))
)

class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    due_date = Column(DateTime)
    categories = relationship("Category",
                              secondary=task_category_association,
                              back_populates="tasks")

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    tasks = relationship("Task",
                         secondary=task_category_association,
                         back_populates="categories")



DB_URL = 'postgresql://postgres:12345@localhost/mero'


engine = create_engine(DB_URL, echo=True)



Base.metadata.create_all(engine)



def get_session():
    with Session(engine) as session:
        yield session

   