import datetime
from fastapi import APIRouter, HTTPException, Depends, FastAPI, BackgroundTasks
from schemas import (
    IncomeDefault,
    Income,
    WasteDefault,
    WasteShow,
    Waste,
    CategoryDefault,
    CategoryShow,
    Category,
    PeriodDefault,
    PeriodShow,
    Period,
    PeriodOfCategoryDefault,
    PeriodOfCategoryShow,
    PeriodOfCategory,
)

from db import get_session
from typing_extensions import TypedDict

logic_router = APIRouter()


@logic_router.post("/category-create")
def category_create(
    category: CategoryDefault, session=Depends(get_session)
) -> TypedDict("Response", {"status": int, "data": Category}):
    category = Category.model_validate(category)
    session.add(category)
    session.commit()
    session.refresh(category)
    return {"status": 200, "data": category}


@logic_router.get("/list-categorys")
def categorys_list(session=Depends(get_session)) -> list[Category]:
    return session.query(Category).all()


@logic_router.get("/category/{category_id}", response_model=CategoryShow)
def category_get(category_id: int, session=Depends(get_session)):
    obj = session.get(Category, category_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="subcategory not found")
    return obj


@logic_router.patch("/category/update/{category_id}")
def category_update(
    category_id: int, category: CategoryDefault, session=Depends(get_session)
) -> Category:
    db_category = session.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="category not found")

    category_data = category.model_dump(exclude_unset=True)
    for key, value in category_data.items():
        setattr(db_category, key, value)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@logic_router.delete("/category/delete/{category_id}")
def category_delete(category_id: int, session=Depends(get_session)):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="category not found")
    session.delete(category)
    session.commit()
    return {"ok": True}


@logic_router.post("/period_of_category-create")
def poc_create(
    poc: PeriodOfCategoryDefault, session=Depends(get_session)
) -> TypedDict("Response", {"status": int, "data": PeriodOfCategory}):
    poc = PeriodOfCategory.model_validate(poc)
    session.add(poc)
    session.commit()
    session.refresh(poc)
    return {"status": 200, "data": poc}


@logic_router.get("/list-pocs")
def pocs_list(session=Depends(get_session)) -> list[PeriodOfCategory]:
    return session.query(PeriodOfCategory).all()


@logic_router.get("/poc/{poc_id}", response_model=PeriodOfCategoryShow)
def poc_get(poc_id: int, session=Depends(get_session)):
    obj = session.get(PeriodOfCategory, poc_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="period of category not found")
    return obj


@logic_router.patch("/poc/update/{poc_id}")
def poc_update(
    poc_id: int, poc: PeriodOfCategoryDefault, session=Depends(get_session)
) -> PeriodOfCategory:
    db_poc = session.get(PeriodOfCategory, poc_id)
    if not db_poc:
        raise HTTPException(status_code=404, detail="period of category not found")

    poc_data = poc.model_dump(exclude_unset=True)
    for key, value in poc_data.items():
        setattr(db_poc, key, value)
    session.add(db_poc)
    session.commit()
    session.refresh(db_poc)
    return db_poc


@logic_router.delete("/poc/delete/{poc_id}")
def poc_delete(poc_id: int, session=Depends(get_session)):
    poc = session.get(PeriodOfCategory, poc_id)
    if not poc:
        raise HTTPException(status_code=404, detail="poc not found")
    session.delete(poc)
    session.commit()
    return {"ok": True}


@logic_router.post("/period-create")
def period_create(
    period: PeriodDefault, session=Depends(get_session)
) -> TypedDict("Response", {"status": int, "data": Period}):
    period = Period.model_validate(period)
    session.add(period)
    session.commit()
    session.refresh(period)
    return {"status": 200, "data": period}


@logic_router.get("/list-periods")
def periods_list(session=Depends(get_session)) -> list[Period]:
    return session.query(Period).all()


@logic_router.get("/period/{period_id}", response_model=PeriodShow)
def period_get(period_id: int, session=Depends(get_session)):
    obj = session.get(Period, period_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="subperiod not found")
    return obj


@logic_router.patch("/period/update/{period_id}")
def period_update(
    period_id: int, period: PeriodDefault, session=Depends(get_session)
) -> Period:
    db_period = session.get(period, period_id)
    if not db_period:
        raise HTTPException(status_code=404, detail="period not found")

    period_data = period.model_dump(exclude_unset=True)
    for key, value in period_data.items():
        setattr(db_period, key, value)
    session.add(db_period)
    session.commit()
    session.refresh(db_period)
    return db_period


@logic_router.delete("/period/delete/{period_id}")
def period_delete(period_id: int, session=Depends(get_session)):
    period = session.get(Period, period_id)
    if not period:
        raise HTTPException(status_code=404, detail="period not found")
    session.delete(period)
    session.commit()
    return {"ok": True}


@logic_router.post("/waste-create")
def waste_create(
    input_data: WasteDefault, session=Depends(get_session)
) -> TypedDict("Response", {"status": int, "data": Waste}):

    date = datetime.datetime.now()
    waste = Waste(poc_id=input_data.poc_id, date=date, value=input_data.value)
    session.add(waste)
    session.commit()
    session.refresh(waste)

    return {"status": 200, "data": waste}


@logic_router.get("/list-wastes")
def wastes_list(session=Depends(get_session)) -> list[Waste]:
    return session.query(Waste).all()


@logic_router.get("/waste/{waste_id}", response_model=WasteShow)
def waste_get(waste_id: int, session=Depends(get_session)):
    obj = session.get(Waste, waste_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="subwaste not found")
    return obj


@logic_router.patch("/waste/update/{waste_id}")
def waste_update(
    waste_id: int, waste: WasteDefault, session=Depends(get_session)
) -> Waste:
    db_waste = session.get(waste, waste_id)
    if not db_waste:
        raise HTTPException(status_code=404, detail="waste not found")

    waste_data = waste.model_dump(exclude_unset=True)
    for key, value in waste_data.items():
        setattr(db_waste, key, value)
    session.add(db_waste)
    session.commit()
    session.refresh(db_waste)
    return db_waste


@logic_router.delete("/waste/delete/{waste_id}")
def waste_delete(waste_id: int, session=Depends(get_session)):
    waste = session.get(Waste, waste_id)
    if not waste:
        raise HTTPException(status_code=404, detail="waste not found")
    session.delete(waste)
    session.commit()
    return {"ok": True}


@logic_router.post("/income-create")
def income_create(
    income: IncomeDefault, session=Depends(get_session)
) -> TypedDict("Response", {"status": int, "data": Income}):
    income = Income.model_validate(income)
    session.add(income)
    session.commit()
    session.refresh(income)
    return {"status": 200, "data": income}


@logic_router.get("/list-incomes")
def income_list(session=Depends(get_session)) -> list[Income]:
    return session.query(Income).all()


@logic_router.get("/income/{income_id}", response_model=Income)
def income_get(income_id: int, session=Depends(get_session)):
    obj = session.get(Income, income_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="subincome not found")
    return obj


@logic_router.patch("/income/update/{income_id}")
def income_update(
    income_id: int, income: IncomeDefault, session=Depends(get_session)
) -> Income:
    db_income = session.get(Income, income_id)
    if not db_income:
        raise HTTPException(status_code=404, detail="income not found")

    income_data = income.model_dump(exclude_unset=True)
    for key, value in income_data.items():
        setattr(db_income, key, value)
    session.add(db_income)
    session.commit()
    session.refresh(db_income)
    return db_income


@logic_router.delete("/income/delete/{income_id}")
def income_delete(income_id: int, session=Depends(get_session)):
    income = session.get(Income, income_id)
    if not income:
        raise HTTPException(status_code=404, detail="income not found")
    session.delete(income)
    session.commit()
    return {"ok": True}
