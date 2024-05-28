import sys
import os
sys.path.insert(0, os.path.realpath(os.path.pardir))
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
from sqlalchemy.orm import Session
from sqlmodel import select, func
import httpx
from models import *
from connection import init_db, get_session


origins = [
    "http://localhost",
    "http://localhost:8080",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CELERY_APP_URL = "http://celery_app:5000"

@app.on_event("startup")
def on_startup():
    init_db()

############################################################################################

def get_user_by_id_or_login(identifier: str, session: Session):
    try:
        user_id = int(identifier)
        user = session.get(User, user_id)
    except ValueError:
        user = session.exec(select(User).where(User.login == identifier)).first()
    return user


@app.post("/users/", response_model=UserCreate)
def create_user(user_create: UserCreate, session: Session = Depends(get_session)):
    statement = select(User).where(User.login == user_create.login)
    result = session.exec(statement)
    existing_user = result.first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this login already exists")
    user = User.model_validate(user_create)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@app.get("/users/{identifier}", response_model=UserCreate)
def read_user(identifier: str, session: Session = Depends(get_session)):
    user = get_user_by_id_or_login(identifier, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/users/", response_model=List[UserCreate])
def list_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users


@app.put("/users/{identifier}", response_model=UserCreate)
def update_user(identifier: str, user_update: UserCreate, session: Session = Depends(get_session)):
    user = get_user_by_id_or_login(identifier, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.login = user_update.login
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@app.delete("/users/{identifier}")
def delete_user(identifier: str, session: Session = Depends(get_session)):
    user = get_user_by_id_or_login(identifier, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}

############################################################################################

def get_ingredient_by_id_or_name(identifier: str, session: Session):
    try:
        ingredient_id = int(identifier)
        ingredient = session.get(Ingredient, ingredient_id)
    except ValueError:
        ingredient = session.exec(select(Ingredient).where(Ingredient.name == identifier)).first()
    return ingredient


@app.post("/ingredients/", response_model=IngredientRead)
def create_ingredient(ingredient_create: IngredientCreate, session: Session = Depends(get_session)):
    statement = select(Ingredient).where(Ingredient.name == ingredient_create.name)
    result = session.exec(statement)
    existing_ingredient = result.first()
    if existing_ingredient:
        raise HTTPException(status_code=400, detail="Ingredient with this name already exists")
    ingredient = Ingredient.model_validate(ingredient_create)
    session.add(ingredient)
    session.commit()
    session.refresh(ingredient)
    return ingredient


@app.get("/ingredients/{identifier}", response_model=IngredientRead)
def read_ingredient(identifier: str, session: Session = Depends(get_session)):
    ingredient = get_ingredient_by_id_or_name(identifier, session)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient


@app.get("/ingredients/", response_model=List[Ingredient])
def list_ingredients(
    type: str = Query(None, description="Filter ingredients by type (base or additive)"),
    session: Session = Depends(get_session)
):
    if type and type.lower() not in ["base", "additive"]:
        raise HTTPException(status_code=400, detail="Invalid type. Must be 'base' or 'additive'.")

    if type:
        filtered_ingredients = session.exec(
            select(Ingredient).where(Ingredient.type == type.lower())
        ).all()
        return filtered_ingredients

    all_ingredients = session.exec(select(Ingredient)).all()
    return all_ingredients


@app.put("/ingredients/{identifier}", response_model=IngredientRead)
def update_ingredient(identifier: str, ingredient_update: IngredientCreate, session: Session = Depends(get_session)):
    ingredient = get_ingredient_by_id_or_name(identifier, session)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    ingredient.name = ingredient_update.name
    ingredient.type = ingredient_update.type
    session.add(ingredient)
    session.commit()
    session.refresh(ingredient)
    return ingredient


@app.delete("/ingredients/{identifier}")
def delete_ingredient(identifier: str, session: Session = Depends(get_session)):
    ingredient = get_ingredient_by_id_or_name(identifier, session)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    session.delete(ingredient)
    session.commit()
    return {"ok": True}

############################################################################################

@app.post("/drinks/", response_model=DrinkRead)
def create_drink(drink_create: DrinkCreate, session: Session = Depends(get_session)):
    user = get_user_by_id_or_login(drink_create.user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    base_ingredient = None
    optional_ingredients = []
    for ing in drink_create.ingredients:
        ingredient = get_ingredient_by_id_or_name(ing.id, session)
        if not ingredient:
            raise HTTPException(status_code=404, detail=f"Ingredient {ing.id} not found")
        if ingredient.type == IngredientType.base:
            if base_ingredient:
                raise HTTPException(status_code=400, detail="Multiple base ingredients not allowed")
            base_ingredient = ingredient
        else:
            optional_ingredients.append(ingredient)

    if not base_ingredient:
        raise HTTPException(status_code=400, detail="Base ingredient required")
    if len(optional_ingredients) > 3:
        raise HTTPException(status_code=400, detail="A drink must have between 0 and 3 additive ingredients")

    drink = Drink(
        user_id=user.id,
        ice=drink_create.ice,
        rating=drink_create.rating,
    )
    session.add(drink)
    session.commit()

    ingredients_stacked = [base_ingredient] + optional_ingredients
    for i, ing in enumerate(drink_create.ingredients):
        link = IngredientDrinkLink(
            drink_id=drink.id,
            ingredient_id=ingredients_stacked[i].id,
            amount=ing.amount,
            n_in_drink=i + 1
        )
        session.add(link)
    session.commit()
    session.refresh(drink)

    ingredient_links = session.exec(select(IngredientDrinkLink).where(IngredientDrinkLink.drink_id == drink.id)).all()
    ingredients = [
        IngredientWithAmountRead(
            id=link.ingredient_id,
            name=session.get(Ingredient, link.ingredient_id).name,
            type=session.get(Ingredient, link.ingredient_id).type,
            amount=link.amount,
            n_in_drink=link.n_in_drink
        )
        for link in ingredient_links
    ]

    return DrinkRead(
        id=drink.id,
        ingredients=ingredients,
        ice=drink.ice,
        rating=drink.rating,
        date_created=drink.date_created
    )


@app.get("/drinks/{drink_id}", response_model=DrinkRead)
def read_drink(drink_id: int, session: Session = Depends(get_session)):
    drink = session.get(Drink, drink_id)
    if not drink:
        raise HTTPException(status_code=404, detail="Drink not found")
    ingredients = [
        IngredientWithAmountRead(
            id=link.ingredient_id,
            name=session.get(Ingredient, link.ingredient_id).name,
            type=session.get(Ingredient, link.ingredient_id).type,
            amount=link.amount,
            n_in_drink=link.n_in_drink
        )
        for link in session.exec(select(IngredientDrinkLink).where(IngredientDrinkLink.drink_id == drink_id))
    ]
    return DrinkRead(
        ingredients=ingredients,
        ice=drink.ice,
        rating=drink.rating,
        date_created=drink.date_created
    )


@app.get("/drinks/", response_model=List[DrinkRead])
def list_drinks(session: Session = Depends(get_session)):
    drinks = session.exec(select(Drink)).all()
    return [
        DrinkRead(
            ingredients=[
                IngredientWithAmountRead(
                    id=link.ingredient_id,
                    name=session.get(Ingredient, link.ingredient_id).name,
                    type=session.get(Ingredient, link.ingredient_id).type,
                    amount=link.amount,
                    n_in_drink=link.n_in_drink
                )
                for link in session.exec(select(IngredientDrinkLink).where(IngredientDrinkLink.drink_id == drink.id))
            ],
            ice=drink.ice,
            rating=drink.rating,
            date_created=drink.date_created
        )
        for drink in drinks
    ]


@app.put("/drinks/{drink_id}", response_model=DrinkRead)
def update_drink(user_identifier: str, drink_id: int, drink_update: DrinkUpdate, session: Session = Depends(get_session)):
    drink = session.get(Drink, drink_id)
    if not drink:
        raise HTTPException(status_code=404, detail="Drink not found")
    
    if not drink.user_id == get_user_by_id_or_login(user_identifier, session).id:
        raise HTTPException(status_code=405, detail="Not allowed")
    
    if drink_update.rating is not None:
        drink.rating = drink_update.rating
    session.add(drink)
    session.commit()
    session.refresh(drink)

    ingredients = [
        IngredientWithAmountRead(
            id=link.ingredient_id,
            name=session.get(Ingredient, link.ingredient_id).name,
            type=session.get(Ingredient, link.ingredient_id).type,
            amount=link.amount,
            n_in_drink=link.n_in_drink
        )
        for link in session.exec(select(IngredientDrinkLink).where(IngredientDrinkLink.drink_id == drink_id))
    ]

    return DrinkRead(
        ingredients=ingredients,
        ice=drink.ice,
        rating=drink.rating,
        date_created=drink.date_created
    )


@app.delete("/drinks/{drink_id}")
def delete_drink(drink_id: int, session: Session = Depends(get_session)):
    drink = session.get(Drink, drink_id)
    if not drink:
        raise HTTPException(status_code=404, detail="Drink not found")

    session.delete(drink)
    session.commit()
    return {"ok": True}


@app.get("/users/{user_identifier}/drinks", response_model=List[DrinkRead])
def get_user_drinks(
    user_identifier: str,
    session: Session = Depends(get_session)
):
    user = get_user_by_id_or_login(user_identifier, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    drinks = session.exec(
        select(Drink).where(Drink.user_id == user.id).order_by(Drink.date_created)
    ).all()

    return [
        DrinkRead(
            ingredients=[
                IngredientWithAmountRead(
                    id=link.ingredient_id,
                    name=session.get(Ingredient, link.ingredient_id).name,
                    type=session.get(Ingredient, link.ingredient_id).type,
                    amount=link.amount,
                    n_in_drink=link.n_in_drink
                )
                for link in session.exec(select(IngredientDrinkLink).where(IngredientDrinkLink.drink_id == drink.id))
            ],
            ice=drink.ice,
            rating=drink.rating,
            date_created=drink.date_created
        )
        for drink in drinks
    ]

############################################################################################

@app.get("/users/{user_identifier}/drinks_count", response_model=int)
def get_user_drinks(
    user_identifier: str,
    session: Session = Depends(get_session)
):
    user = get_user_by_id_or_login(user_identifier, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    count = session.exec(select(func.count(Drink.id)).where(Drink.user_id == user.id)).one()
    return count


@app.get("/ingredients_count", response_model=int)
def get_ingredients_count(session: Session = Depends(get_session)):
    count = session.exec(select(func.count(Ingredient.id))).one()
    return count


@app.get("/drinks_count", response_model=int)
def get_drinks_count(session: Session = Depends(get_session)):
    count = session.exec(select(func.count(Drink.id))).one()
    return count

############################################################################################

@app.post('/api/process')
async def process(ingredients_joined: str = ''):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{CELERY_APP_URL}/api/predict?ingredients_joined={ingredients_joined}")
            response.raise_for_status()
            task_info = response.json()
            return task_info
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
        except Exception as ex:
            raise HTTPException(status_code=500, detail=str(ex))


@app.get('/api/result/{task_id}')
async def result(task_id: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{CELERY_APP_URL}/api/result/{task_id}")
            response.raise_for_status()
            task_info = response.json()
            return task_info
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
        except Exception as ex:
            raise HTTPException(status_code=500, detail=str(ex))


@app.get('/api/status/{task_id}')
async def status(task_id: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{CELERY_APP_URL}/api/status/{task_id}")
            response.raise_for_status()
            task_info = response.json()
            return task_info
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
        except Exception as ex:
            raise HTTPException(status_code=500, detail=str(ex))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)