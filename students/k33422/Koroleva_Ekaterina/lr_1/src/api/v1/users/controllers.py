from typing import Annotated

from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    Path,
    Query,
    status as http_status,
)

from src.core.pydantic.schemes import Message
from src.models import Profile, User
from src.services.auth.dependencies import get_user, get_user_profile
from .repository import repository
from .schemes import (
    ProfileCreate,
    ProfileMe,
    ProfilePartialUpdate,
    ProfileUpdate,
    UserMe,
    UserMultiPublic,
    UserSinglePublic,
)

router = APIRouter(prefix='/users', tags=['Users'])


def concat_user_profile(
    user: User,
    profile: Profile
) -> UserMe:
    return UserMe.model_validate(
        dict(
            **UserMe.model_validate(user.__dict__).model_dump(exclude={'profile'}),
            profile=ProfileMe.model_validate(profile.__dict__).model_dump()
        )
    )


@router.get('/me/', response_model=Annotated[UserMe, Depends()])
async def get_me(
    user: Annotated[User, Depends(get_user_profile)]
):
    return user


@router.post('/me/', response_model=Annotated[UserMe, Depends()])
async def create_me(
    data: Annotated[ProfileCreate, Body()],
    user: Annotated[User, Depends(get_user)]
):
    if user.profile is not None:
        raise HTTPException(
            http_status.HTTP_400_BAD_REQUEST,
            'Profile already created'
        )

    profile = await repository.create(
        dict(
            **data.model_dump(),
            user_id=user.id
        )
    )

    return concat_user_profile(user, profile)


@router.put('/me/', response_model=Annotated[UserMe, Depends()])
async def update_me(
    data: Annotated[ProfileUpdate, Body()],
    user: Annotated[User, Depends(get_user_profile)]
):
    profile = await repository.update(data.model_dump(), user_id=user.id)

    return concat_user_profile(user, profile)


@router.patch('/me/', response_model=Annotated[UserMe, Depends()])
async def partial_update_me(
    data: Annotated[ProfilePartialUpdate, Body()],
    user: Annotated[User, Depends(get_user_profile)]
):
    profile = await repository.update(
        data.model_dump(exclude_none=True),
        user_id=user.id
    )

    return concat_user_profile(user, profile)


@router.delete('/me/', response_model=Annotated[Message, Depends()])
async def delete_me(
    user: Annotated[User, Depends(get_user_profile)]
):
    await repository.delete(user_id=user.id)
    return Message(msg='Success')


@router.get('/', response_model=Annotated[list[UserMultiPublic], Depends()])
async def get_users(
    user: Annotated[User, Depends(get_user)],
    limit: Annotated[int | None, Query()] = 100,
    offset: Annotated[int | None, Query()] = 0
):
    return await repository.get_many_users(
        limit=limit,
        offset=offset,
    )


@router.get('/{pk}/', response_model=Annotated[UserSinglePublic, Depends()])
async def get_user(
    user: Annotated[User, Depends(get_user)],
    pk: Annotated[int, Path()]
):
    user = await repository.get_one_user(id=pk)

    if user is None:
        raise HTTPException(
            http_status.HTTP_404_NOT_FOUND,
            'User not found'
        )

    return user
