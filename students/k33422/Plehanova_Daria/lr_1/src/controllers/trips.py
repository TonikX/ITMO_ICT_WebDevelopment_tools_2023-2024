from datetime import datetime
from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, exists, or_

from src.controllers.auth import get_current_auth_user
from src.db.helper import helper
from src.models import Trip, User, TripBase, TripBasePartial, FavoriuteTrip, TripDetail, UserBaseId, Companion, \
    Status, CompanionBaseId, CompanionBaseDetail, Review, ReviewBaseList, ReviewBaseDetail, ReviewScheme

router = APIRouter(prefix="/trips")


@router.get('/', response_model=Annotated[list[Trip], Depends()])
async def get_trips(
        session: Annotated[AsyncSession, Depends(helper.scoped_session_dependency)],
        search: str | None = None,
        start_location: str | None = None,
        end_location: str | None = None,
        is_actual: bool = None
):
    statement = select(Trip)
    if is_actual:
        # noinspection PyTypeChecker
        statement = statement.where(Trip.start_date > datetime.utcnow())

    if search:
        statement = statement.where(
            or_(
                Trip.description.ilike(f"%{search}%"),
                Trip.end_location.ilike(f"%{search}%")
            )
        )

    if start_location:
        statement = statement.where(Trip.start_location.ilike(start_location))

    if end_location:
        statement = statement.where(Trip.end_location.ilike(end_location))

    res = await session.execute(statement)
    return res.scalars().all()


@router.post('/', response_model=Annotated[Trip, Depends()])
async def create_trip(
        scheme: Annotated[TripBase, Depends()],
        user: Annotated[User, Depends(get_current_auth_user)],
        session: Annotated[AsyncSession, Depends(helper.scoped_session_dependency)]
):
    trip = Trip(**scheme.model_dump(), user_id=user.id)
    session.add(trip)
    await session.commit()
    return trip


@router.get('/{trip_id}/', response_model=Annotated[TripDetail, Depends()])
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


@router.patch('/{trip_id}/', response_model=Annotated[Trip, Depends()])
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

    if trip.user_id != user.id:
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

    if trip.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not an owner"
        )

    await session.delete(trip)
    await session.commit()


@router.get('/{trip_id}/companions/', response_model=Annotated[list[CompanionBaseId], Depends()])
async def get_companions(
        trip_id: int,
        user: Annotated[User, Depends(get_current_auth_user)],
        session: Annotated[AsyncSession, Depends(helper.scoped_session_dependency)],
        status: Status = None,
):
    trip = await session.get(Trip, trip_id)

    if trip is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trip {trip_id} not found!",
        )

    s = (
        select(User, Companion)
        .join(Companion, User.id == Companion.user_id)
        .join(Trip, Companion.trip_id == Trip.id)
        .where(Trip.id == trip_id)
    )

    if status is not None:
        s = s.where(s.c.status == status)

    q = await session.execute(s)

    return [CompanionBaseDetail(**companion.model_dump(), user=user.model_dump()) for user, companion in q.all()]


@router.post('/{trip_id}/companions/', response_model=Annotated[CompanionBaseDetail, Depends()])
async def create_companion(
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

    if trip.user_id == user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are an owner"
        )

    s = await session.execute(
        select(exists().where(Companion.user_id == user.id).where(Companion.trip_id == trip_id))
    )
    r = s.scalar()

    if r:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already a companion for this trip"
        )

    companion = Companion(trip_id=trip_id, user_id=user.id)
    session.add(companion)
    await session.commit()

    return CompanionBaseDetail(**companion.model_dump(), user=user.model_dump())


@router.get('/{trip_id}/companions/{companion_id}/', response_model=Annotated[CompanionBaseDetail, Depends()])
async def get_companion(
        trip_id: int,
        companion_id: int,
        user: Annotated[User, Depends(get_current_auth_user)],
        session: Annotated[AsyncSession, Depends(helper.scoped_session_dependency)]
):
    trip = await session.get(Trip, trip_id)

    if trip is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trip {trip_id} not found!",
        )

    companion = await session.get(Companion, companion_id)

    if companion is None or companion.trip_id != trip_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Companion {companion_id} not found!",
        )

    user = await session.get(User, companion.user_id)

    return CompanionBaseDetail(**companion.model_dump(), user=user.model_dump())


@router.patch('/{trip_id}/companions/{companion_id}/', response_model=Annotated[CompanionBaseDetail, Depends()])
async def update_companion(
        trip_id: int,
        companion_id: int,
        user: Annotated[User, Depends(get_current_auth_user)],
        session: Annotated[AsyncSession, Depends(helper.scoped_session_dependency)],
        status_: Status = None,
):
    trip = await session.get(Trip, trip_id)

    if trip is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trip {trip_id} not found!",
        )

    if trip.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not an owner"
        )

    companion = await session.get(Companion, companion_id)

    if companion is None or companion.trip_id != trip_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Companion {companion_id} not found!",
        )

    user = await session.get(User, companion.user_id)

    if status_ is not None:
        companion.status = status_

    await session.commit()
    return CompanionBaseDetail(**companion.model_dump(), user=user.model_dump())


@router.get("/{trip_id}/reviews/", response_model=Annotated[list[ReviewBaseList], Depends()])
async def get_reviews(
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

    q = await session.execute(
        select(Review).where(Review.trip_id == trip_id)
    )

    return [ReviewBaseList(**i.model_dump()) for i in q.scalars().all()]


@router.post("/{trip_id}/reviews/", response_model=Annotated[ReviewBaseDetail, Depends()])
async def create_reviews(
        trip_id: int,
        scheme: Annotated[ReviewScheme, Depends()],
        user: Annotated[User, Depends(get_current_auth_user)],
        session: Annotated[AsyncSession, Depends(helper.scoped_session_dependency)]
):
    trip = await session.get(Trip, trip_id)

    if trip is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trip {trip_id} not found!",
        )

    if trip.user_id == user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are an owner"
        )

    review = Review(**scheme.model_dump(), user_id=user.id, trip_id=trip_id)
    print(review)

    session.add(review)
    await session.commit()
    return ReviewBaseDetail(**review.model_dump(), user=user.model_dump())


@router.get("/{trip_id}/reviews/{review_id}/", response_model=Annotated[ReviewBaseDetail, Depends()])
async def get_review(
        trip_id: int,
        review_id: int,
        user: Annotated[User, Depends(get_current_auth_user)],
        session: Annotated[AsyncSession, Depends(helper.scoped_session_dependency)]
):
    trip = await session.get(Trip, trip_id)

    if trip is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trip {trip_id} not found!",
        )

    review = await session.get(Review, review_id)

    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review {review_id} not found!",
        )

    return ReviewBaseDetail(**review.model_dump(), user=user.model_dump())
