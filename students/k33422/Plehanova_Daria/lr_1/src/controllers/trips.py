from datetime import datetime
from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.controllers.auth import get_current_auth_user
from src.db.helper import helper
from src.models import Trip, User, TripBase, TripBasePartial, FavoriuteTrip, TripDetail, UserBaseId

router = APIRouter(prefix="/trips")


@router.get('/', response_model=list[Trip])
async def get_trips(
        session: Annotated[AsyncSession, Depends(helper.scoped_session_dependency)],
        is_actual: bool = True
):
    statement = select(Trip)
    if is_actual:
        # noinspection PyTypeChecker
        statement = statement.where(Trip.start_date > datetime.utcnow())

    res = await session.execute(statement)
    return res.scalars().all()


@router.post('/', response_model=Trip)
async def create_trip(
        scheme: Annotated[TripBase, Depends()],
        user: Annotated[User, Depends(get_current_auth_user)],
        session: Annotated[AsyncSession, Depends(helper.scoped_session_dependency)]
):
    trip = Trip(**scheme.model_dump(), user_id=user.id)
    session.add(trip)
    await session.commit()
    return trip


@router.get('/{trip_id}/', response_model=TripDetail)
async def get_trip(
        trip_id: int,
        user: Annotated[User, Depends(get_current_auth_user)],
        session: Annotated[AsyncSession, Depends(helper.scoped_session_dependency)]
):
    trip = await session.get(Trip, trip_id)

    if trip is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trip {trip_id} not found!",
        )

    r = await session.execute(
        select(User)
        .join(FavoriuteTrip, User.id == FavoriuteTrip.user_id)
        .join(Trip, Trip.id == FavoriuteTrip.trip_id)
        .where(Trip.id == trip_id)
    )

    return TripDetail(**trip.model_dump(), liked_by=[UserBaseId(**i.model_dump()) for i in r.scalars().all()])


@router.patch('/{trip_id}/', response_model=Trip)
async def update_trip(
        trip_id: int,
        scheme: Annotated[TripBasePartial, Depends()],
        user: Annotated[User, Depends(get_current_auth_user)],
        session: Annotated[AsyncSession, Depends(helper.scoped_session_dependency)]
):
    trip = await session.get(Trip, trip_id)

    if trip is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trip {trip_id} not found!",
        )

    if trip.user.id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not an owner"
        )

    for name, value in scheme.model_dump(exclude_none=True).items():
        setattr(trip, name, value)

    await session.commit()
    return trip


@router.delete('/{trip_id}/')
async def delete_trip(
        trip_id: int,
        user: Annotated[User, Depends(get_current_auth_user)],
        session: Annotated[AsyncSession, Depends(helper.scoped_session_dependency)]
):
    trip = await session.get(Trip, trip_id)

    if trip is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trip {trip_id} not found!",
        )

    if trip.user.id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not an owner"
        )

    await session.delete(trip)
    await session.commit()
