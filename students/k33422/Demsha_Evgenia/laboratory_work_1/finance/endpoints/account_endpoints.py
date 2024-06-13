from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from connections import get_session
from models import Account
from user_repo.user_endpoints import auth_handler

account_router = APIRouter(dependencies=[Depends(auth_handler.auth_wrapper)])


# Create a new account
@account_router.post("/accounts/", tags=['accounts'])
async def create_account(account: Account, session: Session = Depends(get_session),
                         user=Depends(auth_handler.get_current_user)):
    new_account = Account(name=account.name, balance=account.balance, user_id=user.id)
    session.add(new_account)
    session.commit()
    return {"message": "Account created successfully"}


# Get all accounts for a specific user
@account_router.get("/accounts/list", tags=['accounts'])
async def get_accounts(session: Session = Depends(get_session),
                       user=Depends(auth_handler.get_current_user)):
    user_accounts = session.query(Account).filter(Account.user_id == user.id).all()
    return {"user_id": user.id, "accounts": user_accounts}


# Update an existing account using PATCH method
@account_router.patch("/accounts/{account_id}", tags=['accounts'])
async def update_account(account_id: int, account: Account,
                         session: Session = Depends(get_session),
                         user=Depends(auth_handler.get_current_user)):
    existing_account = session.query(Account).filter_by(id=account_id, user_id=user.id).first()
    if existing_account:
        for field, value in account.dict(exclude_unset=True).items():
            setattr(existing_account, field, value)
        session.commit()
        return {"message": "Account updated successfully"}
    raise HTTPException(status_code=404, detail="Account not found")


# Delete an existing account using DELETE method
@account_router.delete("/accounts/{account_id}", tags=['accounts'])
async def delete_account(account_id: int, session: Session = Depends(get_session),
                         user=Depends(auth_handler.get_current_user)):
    existing_account = session.query(Account).filter_by(id=account_id, user_id=user.id).first()
    if existing_account:
        session.delete(existing_account)
        session.commit()
        return {"message": "Account deleted successfully"}
    raise HTTPException(status_code=404, detail="Account not found")
