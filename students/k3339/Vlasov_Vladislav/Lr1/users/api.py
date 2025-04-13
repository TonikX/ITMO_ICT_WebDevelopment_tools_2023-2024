from typing import Annotated
from typing_extensions import TypedDict
from fastapi import APIRouter, Depends, Header

from users.service import UserService
from users.depends import get_user_service


from users.models import (

    AccountDefault,
    AccountUpdate,
    Account,
    TokenedAccount,

    ProfileUpdate,
    Profile,

    ResponseAccountProfile,
)


user_router = APIRouter()

#Account

@user_router.get("/accounts_list", tags=["Аккаунт"])
async def accounts_list(server: Annotated[UserService, Depends(get_user_service)]) -> list[Account]:
    return await server.get_user_list()


@user_router.get("/account/{account_id}", tags=["Аккаунт"], response_model=ResponseAccountProfile)
async def get_accounts(account_id: int, server: Annotated[UserService, Depends(get_user_service)]) -> Account:
    return await server.get_user(account_id)


@user_router.delete("/account/delete/{account_id}", tags=["Аккаунт"])
async def account_delete(account_id: int, server: Annotated[UserService, Depends(get_user_service)]) -> TypedDict('Response', {"status": int, "message": str}): # type: ignore
    await server.user_delete(account_id)
    return {"status": 201, "message": "deleted"}


@user_router.patch("/account/{account_id}", tags=["Аккаунт"])
async def account_update(account_id: int, account: AccountUpdate, server: Annotated[UserService, Depends(get_user_service)], aut: str = Header(default=None)) -> Account:
    return await server.user_update(account_id, account, aut)


#Profile

@user_router.get("/profiles_list", tags=["Профиль"])
async def profiles_list(server: Annotated[UserService, Depends(get_user_service)]) -> list[Profile]:
    return await server.get_profile_list()


@user_router.get("/profiles_for_account", tags=["Профиль"])
async def profile_for_account(account_id: int, server: Annotated[UserService, Depends(get_user_service)]) -> Profile:
    return await server.get_profile_for_account(account_id)


@user_router.get("/profile/{profile_id}", tags=["Профиль"])
async def get_profiles(profile_id: int, server: Annotated[UserService, Depends(get_user_service)]) -> Profile:
    return await server.get_profile(profile_id)


@user_router.patch("/profile/{profile_id}", tags=["Профиль"])
async def profile_update(profile_id: int, profile: ProfileUpdate, server: Annotated[UserService, Depends(get_user_service)], aut: str = Header(None)) -> Profile:
    return await server.profile_update(profile_id, profile, aut)


#Авторизация и регистрация

@user_router.post("/account", tags=["Аккаунт"])
async def accounts_create(account: AccountDefault, server: Annotated[UserService, Depends(get_user_service)]) -> TypedDict('Response', {"status": int, "data": TokenedAccount}): # type: ignore
    return {"status": 200, "data": await server.post_user(account)}


@user_router.post("/account/sing_in", tags=["Аккаунт"])
async def sing_in(account: AccountDefault, server: Annotated[UserService, Depends(get_user_service)]) -> TypedDict('Response', {"status": int, "data": TokenedAccount}): # type: ignore
    return {"status": 200, "data": await server.sing_in(account)}


@user_router.post("/account/authentication", tags=["Аккаунт"])
async def authentication(token: str, server: Annotated[UserService, Depends(get_user_service)]) -> TypedDict('Response', {"status": int, "data": Account}): # type: ignore
    return {"status": 200, "data": await server.authentication(token)}