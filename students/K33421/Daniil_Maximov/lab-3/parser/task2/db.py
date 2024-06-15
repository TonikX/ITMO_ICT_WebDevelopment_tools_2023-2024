import sqlalchemy
import sqlalchemy.ext.asyncio
import sqlalchemy.orm

engine = sqlalchemy.create_engine("postgresql://postgres:12345@localhost:5432/lab2")
async_engine = sqlalchemy.ext.asyncio.create_async_engine("postgresql+asyncpg://postgres:12345@localhost:5432/lab2")
Base = sqlalchemy.orm.declarative_base()


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


class Article(Base):
    __tablename__ = 'article'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String)


Session = sqlalchemy.orm.sessionmaker(bind=engine)

AsyncSession = sqlalchemy.ext.asyncio.async_sessionmaker(bind=async_engine)
