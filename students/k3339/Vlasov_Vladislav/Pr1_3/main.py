from sqlmodel import select
from typing_extensions import TypedDict
from fastapi import Depends, FastAPI, HTTPException

from connection import get_session, init_db
from model import (
    ProfileDefault,
    Profile,
    BookDefault,
    Book,
    AccountDefault,
    Account,
    ExchangeDefault,
    Exchange,

    ExchangeItem,

    ResponseAccountProfile,
    ResponseExchangeBook,
)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def hello():
    return "Hello, [username]!"


@app.get("/accounts_list")
def accounts_list(session=Depends(get_session)) -> list[Account]:
    return session.exec(select(Account)).all()


@app.get("/account/{account_id}", response_model=ResponseAccountProfile)
def accounts_list(account_id: int, session=Depends(get_session)) -> Account:
    return session.get(Account, account_id)


@app.post("/account")
def accounts_create(account: AccountDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Account}): # type: ignore
    account = Account.model_validate(account)
    session.add(account)
    session.commit()
    session.refresh(account)
    return {"status": 200, "data": account}



@app.delete("/account/delete/{account_id}")
def account_delete(account_id: int, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "message": str}): # type: ignore
    db_account = session.get(Account, account_id)
    if not db_account:
        raise HTTPException(status_code=404, detail="Warrior not found")
    session.delete(db_account)
    session.commit()
    return {"status": 201, "message": "deleted"}


@app.patch("/account/{account_id}")
def account_update(account_id: int, account: AccountDefault, session=Depends(get_session)) -> list[Account]:
    db_account = session.get(Account, account_id)
    if not db_account:
        raise HTTPException(status_code=404, detail="Warrior not found")
    account_data = account.model_dump(exclude_unset=True)
    for key, value in account_data.items():
        setattr(db_account, key, value)
    session.add(db_account)
    session.commit()
    session.refresh(db_account)
    return db_account


@app.get("/profiles_list")
def profiles_list(session=Depends(get_session)) -> list[Profile]:
    return session.exec(select(Profile)).all()


@app.get("/profiles/{profile_id}")
def profile_get(profile_id: int, session=Depends(get_session)) -> Profile:
    return session.get(Profile, profile_id)


@app.post("/profile")
def profile_create(prof: ProfileDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Profile}): # type: ignore
    prof = Profile.model_validate(prof)
    session.add(prof)
    session.commit()
    session.refresh(prof)
    return {"status": 200, "data": prof}


@app.get("/exchange/sender", response_model=list[ResponseExchangeBook])
def get_sender_exchanges(sender_id: int, session=Depends(get_session)) -> list[Exchange]:
    return session.exec(select(Exchange).where(Exchange.sender_id == sender_id)).all()


@app.get("/exchange/receiver", response_model=list[ResponseExchangeBook])
def get_receiver_exchanges(receiver_id: int, session=Depends(get_session)) -> list[Exchange]:
    return session.exec(select(Exchange).where(Exchange.receiver_id == receiver_id)).all()