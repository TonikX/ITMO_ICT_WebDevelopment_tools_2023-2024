from datetime import datetime, timedelta, timezone
import hashlib
import os
import jwt

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from dotenv import load_dotenv
from sqlmodel import SQLModel

from users.models import (

    AccountDefault,
    AccountUpdate,
    Account,
    TokenedAccount,

    ProfileUpdate,
    ProfileDefault,
    Profile,
)


class UserService:
    def __init__(self, session: AsyncSession):
        #Данный сервер - осколок монолита. Такая реализация оправдана только сжатыми сроками (сервер был начат создаваться 13.04 03:11)
        self._session = session

    #________Блок с CRUD для Account

    async def post_user(self, dto: AccountDefault) -> TokenedAccount:
        try:
            account = Account.model_validate(dto)
            account.password = hashlib.sha256(account.password.encode()).hexdigest()
            self._session.add(account)
            await self._session.commit()
            await self._session.refresh(account)

            profile = Profile.model_validate(ProfileDefault(account_id=account.id))
            self._session.add(profile)
            await self._session.commit()
            await self._session.refresh(account)

            token = self._create_token(account.id)
            
            return TokenedAccount(token=token, account=account)
        
        except IntegrityError as e:
            await self._session.rollback()
            
            if 'email' in str(e.orig):
                raise HTTPException(status_code=422, detail="Email already exists.")
            
            elif 'login' in str(e.orig):
                raise HTTPException(status_code=422, detail="Login already exists.")
            

    async def sing_in(self, dto: AccountDefault) -> TokenedAccount:
        query = select(Account).where(Account.login == dto.login)
        account = (await self._session.execute(query)).scalar()
        if account is None or hashlib.sha256(dto.password.encode()).hexdigest() != account.password:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        token = self._create_token(account.id)
        
        return TokenedAccount(token=token, account=account)
    

    async def authentication(self, token: str) -> Account:
        payload = self._decode_token(token)

        query = select(Account).where(Account.id == int(payload["sub"]))
        account = (await self._session.execute(query)).scalar()

        if not account:
            raise HTTPException(
                status_code=401,
                detail="No authenticated user",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return account


    def _create_token(self, account_id) -> str:
        load_dotenv()
        SECRET_KEY = os.getenv('SECRET_KEY')
        return jwt.encode(
            payload={"sub": str(account_id), "iat": datetime.now(timezone.utc).timestamp(), "exp": datetime.now(timezone.utc).timestamp() + 60*60*72},
            key=SECRET_KEY,
            algorithm="HS256",
        )
    

    def _decode_token(self, token) -> str:
        load_dotenv()
        SECRET_KEY = os.getenv('SECRET_KEY')
        try:
            decoded_token = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=["HS256"],
            )

            return decoded_token
        
        except (jwt.InvalidTokenError, ValueError):
            raise HTTPException(
                status_code=401,
                detail="Token has expired or invalid",
                headers={"WWW-Authenticate": "Bearer"},
            )


    async def get_user_list(self) -> list[Account]:
        return (await self._session.execute(select(Account))).scalars().all()

    async def get_user(self, account_id) -> Account:
        account = (await self._session.execute(select(Account).options(selectinload(Account.profile)).where(Account.id == account_id))).scalars().first()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        return account

    async def user_update(self, account_id: int, dto: AccountUpdate, authorization: str) -> Account:
        
        print(authorization)

        if (await self.authentication(authorization)).id != account_id:
            raise HTTPException(status_code=403, detail="Invalid authentication")

        db_account = await self._session.get(Account, account_id)
        if not db_account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        account_data = dto.model_dump(exclude_unset=True)
        account_data["password"] = hashlib.sha256(account_data["password"].encode()).hexdigest()
        for key, value in account_data.items():
            setattr(db_account, key, value)

        await self._session.commit()
        await self._session.refresh(db_account)
        return db_account


    async def user_delete(self, account_id: int): # type: ignore
        db_account = await self._session.get(Account, account_id)
        if not db_account:
            raise HTTPException(status_code=404, detail="Account not found")
        await self._session.delete(db_account)
        await self._session.commit()


    #________Блок с CRUD (RU) для Profile

    async def get_profile_for_account(self, account_id) -> Profile:
        profile = (await self._session.execute(select(Profile).where(Profile.account_id == account_id))).scalars().first()
        if not profile:
            raise HTTPException(status_code=404, detail="Account not found")
        return profile


    async def get_profile_list(self) -> list[Profile]:
        return (await self._session.execute(select(Profile))).scalars().all()


    async def get_profile(self, profile_id) -> Profile:
        profile = await self._session.get(Profile, profile_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Account not found")
        return profile
    

    async def profile_update(self, profile_id: int, dto: ProfileUpdate, authorization: str) -> Profile:
        db_profile = await self._session.get(Profile, profile_id)

        if not db_profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        if (await self.authentication(authorization)).id != db_profile.account_id:
            raise HTTPException(status_code=403, detail="Invalid authentication")
        
        profile_data = dto.model_dump(exclude_unset=True)
        for key, value in profile_data.items():
            setattr(db_profile, key, value)

        await self._session.commit()
        await self._session.refresh(db_profile)
        return db_profile