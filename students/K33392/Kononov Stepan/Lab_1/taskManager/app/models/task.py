from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, Text
from sqlalchemy.orm import relationship

from app.database import Base

task_category_association = Table(
    'task_category', Base.metadata,
    Column('task_id', Integer, ForeignKey('tasks.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    deadline = Column(DateTime)
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    priority_id = Column(Integer, ForeignKey("priorities.id"))

    owner = relationship("User", back_populates="tasks")
    project = relationship("Project", back_populates="tasks")
    priority = relationship("Priority", back_populates="tasks")
    categories = relationship("Category", secondary=task_category_association, back_populates="tasks")
