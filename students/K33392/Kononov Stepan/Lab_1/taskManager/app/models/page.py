from sqlalchemy import Column, Integer, String

from app.database import Base


class Page(Base):
    __tablename__ = 'pages'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    title = Column(String)

    def __repr__(self):
        return f"<Page(url={self.url}, title={self.title})>"
