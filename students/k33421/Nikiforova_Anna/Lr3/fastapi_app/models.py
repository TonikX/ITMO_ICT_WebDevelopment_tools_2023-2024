from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from typing import List, Optional
from datetime import datetime
from pydantic import validator, root_validator


class IngredientType(str, Enum):
    base = "base"
    additive = "additive"


class IngredientDrinkLink(SQLModel, table=True):
    drink_id: Optional[int] = Field(default=None, foreign_key="drink.id", primary_key=True)
    ingredient_id: Optional[int] = Field(default=None, foreign_key="ingredient.id", primary_key=True)
    amount: int = Field(default=1, ge=1, le=5)
    n_in_drink: int


class Ingredient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column_kwargs={"unique": True}, index=True)
    type: IngredientType
    
    drinks: List["Drink"] = Relationship(
        back_populates="ingredients", link_model=IngredientDrinkLink
    )


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    login: str = Field(sa_column_kwargs={"unique": True}, index=True)
    
    drinks: List["Drink"] = Relationship(back_populates="user")


class Drink(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    date_created: datetime = Field(default_factory=datetime.now)
    ice: bool = Field(default=False)
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    
    user: User = Relationship(back_populates="drinks")
    ingredients: List["Ingredient"] = Relationship(
        back_populates="drinks", link_model=IngredientDrinkLink
    )

    @root_validator(pre=True)
    def validate_ingredients(cls, values):
        ingredients = values.get('ingredients', [])
        base_count = sum(1 for ingredient in ingredients if ingredient.type == IngredientType.base)
        additive_count = sum(1 for ingredient in ingredients if ingredient.type == IngredientType.additive)

        if base_count != 1:
            raise ValueError('A drink must have exactly one base ingredient.')
        if not (0 <= additive_count <= 3):
            raise ValueError('A drink must have between 0 and 3 additive ingredients.')

        return values

############################################################################################

class UserCreate(SQLModel, table=False):
    login: str

############################################################################################

class DrinkCreate(SQLModel, table=False):
    user_id: str
    ingredients: List['IngredientWithAmountCreate']
    ice: bool = False
    rating: Optional[int] = None


class DrinkRead(SQLModel, table=False):
    ingredients: List["IngredientWithAmountRead"] 
    ice: bool
    rating: Optional[int] = None
    date_created: datetime
    

class DrinkUpdate(SQLModel, table=False):
    rating: Optional[int] = None

############################################################################################

class IngredientCreate(SQLModel, table=False): 
    name: str
    type: IngredientType
    
    
class IngredientRead(SQLModel, table=False): 
    name: str
    type: IngredientType
    
    
class IngredientWithAmountRead(SQLModel, table=False): 
    name: str
    type: IngredientType
    amount: int
    n_in_drink: int
    
    
class IngredientWithAmountCreate(SQLModel, table=False): 
    id: str
    amount: int = 1
    
############################################################################################

class Task(SQLModel, table=False):
    task_id: str
    status: str


class Prediction(SQLModel, table=False):
    task_id: str
    status: str
    result: str