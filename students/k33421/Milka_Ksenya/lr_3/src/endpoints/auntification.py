import typing as tp

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from .. import dependencies, models, schemas
from ..services.auntification import check_password, create_jwt, hash_password

router = APIRouter(prefix="/auth", tags=["Auntification"])


@router.post("/signUp", response_model=str)
async def sign_up(
    schema: schemas.Sign,
    session: dependencies.AsyncSession = Depends(dependencies.get_session)
):
    user = models.User(
        username=schema.username,
        password=hash_password(schema.password),
    )
    session.add(user)
    await session.commit()

    return "OK"


@router.post("/signIn", response_model=schemas.AccessToken)
async def sign_in(
    schema: schemas.Sign,
    session: dependencies.AsyncSession = Depends(dependencies.get_session)
):
    statement = select(models.User).where(models.User.username == schema.username)  # noqa
    result = await session.exec(statement)
    user = result.one_or_none()

    if user is None or not check_password(schema.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password")

    return schemas.AccessToken(access_token=create_jwt(user.id))  # type: ignore


@router.post("/changePassword", response_model=str)
async def change_password(
    schema: schemas.ChangePassword,
    user: tp.Annotated[type[models.User], Depends(dependencies.get_user)],
    session: dependencies.AsyncSession = Depends(dependencies.get_session),
):
    if not check_password(schema.old_password, user.password):  # noqa
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password")

    user.password = hash_password(schema.new_password)
    session.add(user)
    await session.commit()

    return "OK"
