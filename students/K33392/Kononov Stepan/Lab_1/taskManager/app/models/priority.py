from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Priority(Base):
    __tablename__ = "priorities"
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String, index=True)
    description = Column(String)

    tasks = relationship("Task", back_populates="priority")
