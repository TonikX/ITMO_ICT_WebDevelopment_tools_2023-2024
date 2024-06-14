from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from db import get_session
from models.categories import Category
from models.links import CategoryOperationLink
from models.operations import Operation

categoryRouter = APIRouter(prefix="", tags=["category"])  # отвечает за swagger


@categoryRouter.get("/categories/m")
async def get_categories_many(session=Depends(get_session)):
    cols = session.query(CategoryOperationLink).all()
    resp = list()
    for col in cols:
        operation = session.exec(select(Operation).where(Operation.id == col.operation_id)).one()
        category = session.exec(select(Category).where(Category.id == col.category_id)).one()
        resp.append({"operation": operation, "category": category})
    return resp


@categoryRouter.get("/categories/", response_model=list[Category])  # response_model отвечает за тип отображаемых и возвращаемых значений - нужно для отображения полей и вложенных моделей
async def get_categories(session=Depends(get_session)):  # в параметры передаем сессию для выполнения запросов в БД
    categories = session.query(Category).all()  # внутри сессии выполняется запрос select на выборку всех категорий
    return categories


@categoryRouter.get("/categories/{category_id}", response_model=Category)
async def get_category(category_id: int, session=Depends(get_session)):
    category = session.query(Category).filter_by(id=category_id).first()  # выполняется запрос на выборку с фильтром по id и берется первая запись
    return category


@categoryRouter.post("/categories/")  # выполняется пост запрос на создание записи
async def create_category(category: Category, session=Depends(get_session)):
    category = Category.validate(category)  # валидация переданного json и маппинг
    category.id = None  # устанавливаем в None для автоинкремента id
    session.add(category)  # добавляем
    session.commit()  # подтверждаем
    session.refresh(category)  # обновляем запись с дефолтными значениями и сгенерированным id
    return category


@categoryRouter.patch("/categories/{category_id}")  # выполняется патч запрос на частичное обновление записи (пут запрос на полное)
async def update_category(category: Category, category_id: int, session=Depends(get_session)):
    category = Category.validate(category)
    category_from_db = session.query(Category).filter_by(id=category_id).first()
    if category_from_db is None:  # если запись с переданным id не найдена, то возвращаем исключение
        raise HTTPException(status_code=404, detail="No such category")
    category_data = category.model_dump(exclude_unset=True)  # полученная модель в параметрах преобразуется в json с получением только измененных полей (флаг exclude_unset)
    for key, value in category_data.items():  # проходимся в цикле по всем полям
        setattr(category_from_db, key, value)  # обновляем все указанные поля
    session.add(category_from_db)
    session.commit()
    session.refresh(category_from_db)
    return category_from_db


@categoryRouter.delete("/categories/{category_id}")  # при делит запросе удаляется запись с переданным id
async def delete_category(category_id: int, session=Depends(get_session)):
    session.query(Category).filter_by(id=category_id).delete()  # если записей каким-то образом с данным id несколько, то удалятся все
    session.commit()
    return "Deleted"
