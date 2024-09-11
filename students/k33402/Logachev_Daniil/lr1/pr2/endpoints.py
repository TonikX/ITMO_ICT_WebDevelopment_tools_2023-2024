import datetime
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from schemas import (Salary, SalaryDB, SalaryDisplay,SalaryPeriod, SalaryPeriodDisplay, SalaryPeriodDB,
                     SalaryPeriodForUser, SalaryPeriodForUserDB, SalaryPeriodForUserDisplay,
                     WasteDB, WasteDisplay, Waste, WastePeriodDisplay, WastePeriodDB, WastePeriod,
                     WastePeriodForUser, WastePeriodForUserDB, WastePeriodForUserDisplay)

from db import get_session
from typing_extensions import TypedDict

logic_router = APIRouter()


@logic_router.post("/waste_period_for_user-create")
def wp_user_create(wp_user: WastePeriodForUserDB, session=Depends(get_session)) \
        -> TypedDict('Response', {"status": int,
                                  "data": WastePeriodForUser}):
    wp_user = WastePeriodForUser.model_validate(wp_user)
    session.add(wp_user)
    session.commit()
    session.refresh(wp_user)
    return {"status": 200, "data": wp_user}

@logic_router.get("/list-waste_period_for_user")
def wp_users_list(session=Depends(get_session)) -> list[WastePeriodForUser]:
    return session.query(WastePeriodForUser).all()


@logic_router.get("/waste_period_for_user/{wp_user_id}",  response_model=WastePeriodForUserDisplay)
def wp_user_get(wp_user_id: int, session=Depends(get_session)):
    obj = session.get(WastePeriodForUser, wp_user_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="waste period not found")
    return obj


@logic_router.patch("/waste_period_for_user/update/{wp_user_id}")
def wp_user_update(wp_user_id: int, wp_user: WastePeriodForUserDB, session=Depends(get_session)) -> \
        WastePeriodForUser:
    db_wp_user = session.get(WastePeriodForUser, wp_user_id)
    if not db_wp_user:
        raise HTTPException(status_code=404, detail="waste period not found")

    wp_user_data = wp_user.model_dump(exclude_unset=True)
    for key, value in wp_user_data.items():
        setattr(db_wp_user, key, value)
    session.add(db_wp_user)
    session.commit()
    session.refresh(db_wp_user)
    return db_wp_user


@logic_router.delete("/waste_period_for_user/delete/{wp_user_id}")
def wp_user_delete(wp_user_id: int, session=Depends(get_session)):
    wp_user = session.get(WastePeriodForUser, wp_user_id)
    if not wp_user:
        raise HTTPException(status_code=404, detail="wp_user not found")
    session.delete(wp_user)
    session.commit()
    return {"ok": True}

#########

@logic_router.post("/salary_period_for_user-create")
def sp_user_create(sp_user: SalaryPeriodForUserDB, session=Depends(get_session)) \
        -> TypedDict('Response', {"status": int,
                                  "data": SalaryPeriodForUser}):
    sp_user = SalaryPeriodForUser.model_validate(sp_user)
    session.add(sp_user)
    session.commit()
    session.refresh(sp_user)
    return {"status": 200, "data": sp_user}


@logic_router.get("/list-salary_period_for_user")
def sp_users_list(session=Depends(get_session)) -> list[SalaryPeriodForUser]:
    return session.query(SalaryPeriodForUser).all()


@logic_router.get("/salary_period_for_user/{sp_user_id}",  response_model=SalaryPeriodForUserDisplay)
def sp_user_get(sp_user_id: int, session=Depends(get_session)):
    obj = session.get(SalaryPeriodForUser, sp_user_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="salary period not found")
    return obj


@logic_router.patch("/salary_period_for_user/update/{sp_user_id}")
def sp_user_update(sp_user_id: int, sp_user: SalaryPeriodForUserDB, session=Depends(get_session)) -> \
        SalaryPeriodForUser:
    db_sp_user = session.get(SalaryPeriodForUser, sp_user_id)
    if not db_sp_user:
        raise HTTPException(status_code=404, detail="salary period not found")

    sp_user_data = sp_user.model_dump(exclude_unset=True)
    for key, value in sp_user_data.items():
        setattr(db_sp_user, key, value)
    session.add(db_sp_user)
    session.commit()
    session.refresh(db_sp_user)
    return db_sp_user


@logic_router.delete("/salary_period_for_user/delete/{sp_user_id}")
def sp_user_delete(sp_user_id: int, session=Depends(get_session)):
    sp_user = session.get(SalaryPeriodForUser, sp_user_id)
    if not sp_user:
        raise HTTPException(status_code=404, detail="sp_user not found")
    session.delete(sp_user)
    session.commit()
    return {"ok": True}


########

@logic_router.post("/waste_period-create")
def waste_period_create(period: WastePeriodDB, session=Depends(get_session)) \
        -> TypedDict('Response', {"status": int,
                                  "data": WastePeriod}):
    period = WastePeriod.model_validate(period)
    session.add(period)
    session.commit()
    session.refresh(period)
    return {"status": 200, "data": period}


@logic_router.get("/list-waste_period")
def waste_periods_list(session=Depends(get_session)) -> list[WastePeriod]:
    return session.query(WastePeriod).all()


@logic_router.get("/waste_period/{period_id}",  response_model=WastePeriodDisplay)
def waste_period_get(period_id: int, session=Depends(get_session)):
    obj = session.get(WastePeriod, period_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="subperiod not found")
    return obj


@logic_router.patch("/waste_period/update/{period_id}")
def waste_period_update(period_id: int, period: WastePeriodDB, session=Depends(get_session)) -> WastePeriod:
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


@logic_router.delete("/waste_period/delete/{period_id}")
def waste_period_delete(period_id: int, session=Depends(get_session)):
    period = session.get(WastePeriod, period_id)
    if not period:
        raise HTTPException(status_code=404, detail="period not found")
    session.delete(period)
    session.commit()
    return {"ok": True}

########

@logic_router.post("/salary_period-create")
def salary_period_create(period: SalaryPeriodDB, session=Depends(get_session)) \
        -> TypedDict('Response', {"status": int,
                                  "data": SalaryPeriod}):
    period = SalaryPeriod.model_validate(period)
    session.add(period)
    session.commit()
    session.refresh(period)
    return {"status": 200, "data": period}


@logic_router.get("/list-salary_period")
def salary_periods_list(session=Depends(get_session)) -> list[SalaryPeriod]:
    return session.query(SalaryPeriod).all()


@logic_router.get("/salary_period/{period_id}",  response_model=SalaryPeriodDisplay)
def salary_period_get(period_id: int, session=Depends(get_session)):
    obj = session.get(SalaryPeriod, period_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="subperiod not found")
    return obj


@logic_router.patch("/salary_period/update/{period_id}")
def salary_period_update(period_id: int, period: SalaryPeriodDB, session=Depends(get_session)) -> SalaryPeriod:
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


@logic_router.delete("/salary_period/delete/{period_id}")
def salary_period_delete(period_id: int, session=Depends(get_session)):
    period = session.get(SalaryPeriod, period_id)
    if not period:
        raise HTTPException(status_code=404, detail="period not found")
    session.delete(period)
    session.commit()
    return {"ok": True}

###############

@logic_router.post("/waste-create")
def waste_create(input_data: WasteDB, session=Depends(get_session)) \
        -> TypedDict('Response', {"status": int,
                                  "data": Waste}):

    date = datetime.datetime.now()
    waste = Waste(type=input_data.type, date=date, value=input_data.value,
                  waste_period_for_user_id=input_data.waste_period_for_user_id)
    session.add(waste)
    session.commit()
    session.refresh(waste)

    return {"status": 200, "data": waste}


@logic_router.get("/list-wastes")
def wastes_list(session=Depends(get_session)) -> list[Waste]:
    return session.query(Waste).all()


@logic_router.get("/waste/{waste_id}",  response_model=WasteDisplay)
def waste_get(waste_id: int, session=Depends(get_session)):
    obj = session.get(Waste, waste_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="waste not found")
    return obj


@logic_router.patch("/waste/update/{waste_id}")
def waste_update(waste_id: int, waste: WasteDB, session=Depends(get_session)) -> Waste:
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

#########

@logic_router.post("/salary-create")
def salary_create(input_data: SalaryDB, session=Depends(get_session)) \
        -> TypedDict('Response', {"status": int,
                                  "data": Salary}):

    date = datetime.datetime.now()
    salary = Salary(legal=input_data.legal, salary_period_for_user_id=input_data.salary_period_for_user_id,
                    date=date, value=input_data.value)
    session.add(salary)
    session.commit()
    session.refresh(salary)
    return {"status": 200, "data": salary}


@logic_router.get("/list-salarys")
def salary_list(session=Depends(get_session)) -> list[Salary]:
    return session.query(Salary).all()


@logic_router.get("/salary/{salary_id}", response_model=SalaryDisplay)
def salary_get(salary_id: int, session=Depends(get_session)):
    obj = session.get(Salary, salary_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="salary not found")
    return obj


@logic_router.patch("/salary/update/{salary_id}")
def salary_update(salary_id: int, salary: SalaryDB, session=Depends(get_session)) -> Salary:
    db_salary = session.get(Salary, salary_id)
    if not db_salary:
        raise HTTPException(status_code=404, detail="salary not found")

    salary_data = salary.model_dump(exclude_unset=True)
    for key, value in salary_data.items():
        setattr(db_salary, key, value)
    session.add(db_salary)
    session.commit()
    session.refresh(db_salary)
    return db_salary


@logic_router.delete("/salary/delete/{salary_id}")
def salary_delete(salary_id: int, session=Depends(get_session)):
    salary = session.get(Salary, salary_id)
    if not salary:
        raise HTTPException(status_code=404, detail="salary not found")
    session.delete(salary)
    session.commit()
    return {"ok": True}