from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from connection import Base

# Таблица many-to-many между titles и categories
recipe_categories = Table(
    'recipe_categories', Base.metadata,
    Column('recipe_id', Integer, ForeignKey('titles.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    author_url = Column(String, nullable=True)

    # Relationship to Titles
    titles = relationship('Title', back_populates='author')


class Title(Base):
    __tablename__ = 'titles'
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    ingredients = Column(Integer, nullable=False)
    servings = Column(Integer, nullable=False)
    cook_time = Column(String, nullable=True)
    author_id = Column(Integer, ForeignKey('author.id'), nullable=False)
    cur_url = Column(String, nullable=True)

    # Relationship to Author
    author = relationship('Author', back_populates='titles')

    # Relationship to Categories
    categories = relationship('Category', secondary=recipe_categories, back_populates='recipes')


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    url = Column(String, nullable=True)

    # Relationship to Titles
    recipes = relationship('Title', secondary=recipe_categories, back_populates='categories')
