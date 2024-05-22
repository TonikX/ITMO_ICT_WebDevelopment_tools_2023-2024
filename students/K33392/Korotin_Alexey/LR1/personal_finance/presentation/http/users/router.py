from typing import Collection, List, Optional

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.responses import Response
from starlette import status

from personal_finance.application.auth.crypt import verify_password
from personal_finance.application.auth.service import get_current_user, encode_token
from personal_finance.application.exceptions import NotFoundException, ConflictException
from .dto import UserReadDto, UserCreateDto, UserUpdateDto, JwtDto, LoginDto
from personal_finance.application.ioc import IocContainer
from personal_finance.application.users.dto import ReadUserDto, WriteUserDto
from personal_finance.application.users.service import UserService
from .. import router

user_router = APIRouter()


@user_router.get("/", status_code=status.HTTP_200_OK)
def get_users(user_service: UserService = Depends(IocContainer.service['UserService'])) -> List[UserReadDto]:
    collection: Collection[ReadUserDto] = user_service.find_all()

    return list(map(UserReadDto.from_app_dto, collection))


@user_router.get("/{user_id}", status_code=status.HTTP_200_OK, responses={
    status.HTTP_404_NOT_FOUND: {

    }
})
def get_user(user_id: int,
             user_service: UserService = Depends(IocContainer.service['UserService'])) -> Optional[UserReadDto]:
    try:
        user: ReadUserDto = user_service.find_by_id(user_id)
        return UserReadDto.from_app_dto(user)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": e.message})


@user_router.post('/register', status_code=status.HTTP_201_CREATED, responses={
    status.HTTP_409_CONFLICT: {}
})
def register(user: UserCreateDto,
             user_service: UserService = Depends(IocContainer.service['UserService'])) -> JwtDto:
    user = UserCreateDto.model_validate(user)
    user_dto: WriteUserDto = WriteUserDto(**user.model_dump())
    try:
        created_user: ReadUserDto = user_service.save(user_dto)
        return JwtDto(token=encode_token(created_user.id))
    except ConflictException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"message": e.message})


@user_router.put("/{user_id}", status_code=status.HTTP_200_OK, responses={
    status.HTTP_403_FORBIDDEN: {},
    status.HTTP_404_NOT_FOUND: {},
    status.HTTP_409_CONFLICT: {}
})
def update_account_info(user_id: int,
                        user: UserUpdateDto,
                        user_service: UserService = Depends(IocContainer.service['UserService']),
                        current_user: ReadUserDto = Depends(get_current_user)) -> UserReadDto:
    user = UserUpdateDto.model_validate(user)
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    user_dto: WriteUserDto = WriteUserDto(**user.model_dump())
    try:
        updated_user: ReadUserDto = user_service.update(user_id, user_dto)
        return UserReadDto.from_app_dto(updated_user)
    except ConflictException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"message": e.message})
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": e.message})


@user_router.post('/login', status_code=status.HTTP_200_OK, responses={
    status.HTTP_401_UNAUTHORIZED: {}
})
def login(login_data: LoginDto,
          user_service: UserService = Depends(IocContainer.service['UserService'])):
    try:
        user: ReadUserDto = user_service.find_by_login(login_data.login)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"message": e.message})

    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    token = encode_token(user.id)
    return JwtDto(token=token)


@user_router.get("/me", status_code=status.HTTP_200_OK, responses={
    status.HTTP_401_UNAUTHORIZED: {}
})
def get_self(current_user: ReadUserDto = Depends(get_current_user)) -> UserReadDto:
    return UserReadDto.from_app_dto(current_user)
