from sqlalchemy import Column, Integer, Float, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy.types import TypeDecorator
from database import engine


Base = declarative_base()

class LowercasedString(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return value.lower() if isinstance(value, str) else value
    

class NullableStringValidator(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return value if value != '' else None


class FloatStringValidator(TypeDecorator):
    impl = Float
    cache_ok = True

    def process_bind_param(self, value, dialect):
        # Validate and convert string representation of float
        if value == '':
            return None
        if isinstance(value, str):
            value = value.replace(',', '.')
        return value


ingredient_coctail_link = Table(
    "ingredient_coctail",
    Base.metadata,
    Column("ingredient_id", Integer, ForeignKey("ingredient.id"), primary_key=True),
    Column("coctail_id", Integer, ForeignKey("coctail.id"), primary_key=True),
    Column("unit", String), 
    Column("unit_value", FloatStringValidator),
    Column("parts", NullableStringValidator) 
)


property_coctail_link = Table(
    "properties_coctail",
    Base.metadata,
    Column("properties_id", Integer, ForeignKey("property.id"), primary_key=True),
    Column("coctail_id", Integer, ForeignKey("coctail.id"), primary_key=True),
)


class Ingredient(Base):
    __tablename__ = "ingredient"

    id = Column(Integer, primary_key=True)
    name = Column(LowercasedString)
    coctails = relationship("Coctail", secondary=ingredient_coctail_link, back_populates="ingredients")


class Property(Base):
    __tablename__ = "property"

    id = Column(Integer, primary_key=True)
    property_name = Column(String)
    class_name = Column(String)
    name = Column(String)
    value = Column(NullableStringValidator, nullable=True)
    coctails = relationship("Coctail", secondary=property_coctail_link, back_populates="properties")


class Coctail(Base):
    __tablename__ = "coctail"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    name_ru = Column(NullableStringValidator, nullable=True)
    detail_text = Column(String)
    steps = Column(String)
    price = Column(FloatStringValidator, nullable=True)
    properties = relationship("Property", secondary=property_coctail_link, back_populates="coctails")
    ingredients = relationship("Ingredient", secondary=ingredient_coctail_link, back_populates="coctails")



def init_db(drop=True) -> None:
    if drop:
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    

if __name__ == "__main__":
    init_db()