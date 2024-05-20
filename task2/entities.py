import sqlalchemy
import sqlalchemy.ext.asyncio
import sqlalchemy.orm

engine = sqlalchemy.create_engine("postgresql://postgres:password@localhost:5432/lab2")
async_engine = sqlalchemy.ext.asyncio.create_async_engine("postgresql+asyncpg://postgres:password@localhost:5432/lab2")
Base = sqlalchemy.orm.declarative_base()


def drop_create_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


class Article(Base):
    __tablename__ = 'article'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    url = sqlalchemy.Column(sqlalchemy.String)

    def __repr__(self):
        return f'<Article(title={self.title}, url={self.url})>'


Session = sqlalchemy.orm.sessionmaker(bind=engine)

AsyncSession = sqlalchemy.ext.asyncio.async_sessionmaker(bind=async_engine)
