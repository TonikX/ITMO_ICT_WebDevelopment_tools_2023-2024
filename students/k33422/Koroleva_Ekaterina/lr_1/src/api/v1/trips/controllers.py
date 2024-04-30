from typing import Annotated

from fastapi import (APIRouter, Body, Depends, HTTPException, Path, status)

from src.core.pydantic.schemes import Message
from src.models import User
from src.services.auth import get_user, get_user_profile
from src.services.pagination import get_pagination_params, PaginationParams
from .filters import FilterParams, get_filter_params, get_search_param, SearchParam
from .repository import repository
from .schemes import (
    CreateMyTrip,
    MyTripMulti,
    MyTripSingle,
    MyTripSingleAfterOperation,
    PartialUpdateMyTrip, TripMulti,
    TripSingle, UpdateMyTrip,
)

router = APIRouter(prefix='/trips', tags=['Trips'])


@router.get('/', response_model=Annotated[list[TripMulti], Depends()])
async def get_trips(
    user: Annotated[User, Depends(get_user)],
    filter_params: Annotated[FilterParams, Depends(get_filter_params)],
    search_param: Annotated[SearchParam, Depends(get_search_param)],
    pag_params: Annotated[PaginationParams, Depends(get_pagination_params)]
):
    return await repository.get_many_trips_filters(
        filter_params=filter_params,
        search_param=search_param,
        pag_params=pag_params
    )


@router.get('/my/', response_model=Annotated[list[MyTripMulti], Depends()])
async def get_my_trips(
    user: Annotated[User, Depends(get_user_profile)],
    filter_params: Annotated[FilterParams, Depends(get_filter_params)],
    search_param: Annotated[SearchParam, Depends(get_search_param)],
    pag_params: Annotated[PaginationParams, Depends(get_pagination_params)]
):
    return await repository.get_many_trips_filters(
        filter_params=filter_params,
        search_param=search_param,
        pag_params=pag_params,
        profile_id=user.profile.id
    )


@router.post('/my/', response_model=Annotated[MyTripSingleAfterOperation, Depends()])
async def create_my_trip(
    data: Annotated[CreateMyTrip, Body()],
    user: Annotated[User, Depends(get_user_profile)]
):
    return await repository.create(
        dict(
            **data.model_dump(),
            profile_id=user.profile.id
        )
    )


@router.get('/my/{pk}/', response_model=Annotated[MyTripSingle, Depends()])
async def get_my_trip(
    user: Annotated[User, Depends(get_user_profile)],
    pk: Annotated[int, Path()]
):
    trip = await repository.get_one_trip(id=pk, profile_id=user.profile.id)

    if trip is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            'Trip not found'
        )

    return trip


@router.put('/my/{pk}/', response_model=Annotated[MyTripSingleAfterOperation, Depends()])
async def update_my_trip(
    data: Annotated[UpdateMyTrip, Body()],
    user: Annotated[User, Depends(get_user_profile)],
    pk: Annotated[int, Path()]
):
    trip = await repository.get_one_trip(id=pk, profile_id=user.profile.id)

    if trip is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            'Trip not found'
        )

    result = await repository.update(
        data.model_dump(),
        id=pk,
        profile_id=user.profile.id
    )

    return result


@router.patch('/my/{pk}/', response_model=Annotated[MyTripSingleAfterOperation, Depends()])
async def partial_update_my_trip(
    data: Annotated[PartialUpdateMyTrip, Body()],
    user: Annotated[User, Depends(get_user_profile)],
    pk: Annotated[int, Path()]
):
    trip = await repository.get_one_trip(id=pk, profile_id=user.profile.id)

    if trip is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            'Trip not found'
        )

    result = await repository.update(
        data.model_dump(exclude_none=True),
        id=pk,
        profile_id=user.profile.id
    )

    return result


@router.delete('/my/{pk}/', response_model=Annotated[Message, Depends()])
async def delete_my_trip(
    user: Annotated[User, Depends(get_user_profile)],
    pk: Annotated[int, Path()]
):
    trip = await repository.get_one_trip(id=pk, profile_id=user.profile.id)

    if trip is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            'Trip not found'
        )

    await repository.delete(id=pk, profile_id=user.profile.id)

    return Message(msg='Success')


@router.get('/{pk}/', response_model=Annotated[TripSingle, Depends()])
async def get_trip(
    user: Annotated[User, Depends(get_user)],
    pk: Annotated[int, Path()]
):
    trip = await repository.get_one_trip(id=pk)

    if trip is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            'Trip not found'
        )

    return trip


@router.post('/{pk}/join/', response_model=Annotated[Message, Depends()])
async def join_trip(
    user: Annotated[User, Depends(get_user_profile)],
    pk: Annotated[int, Path()]
):
    trip = await repository.get_one_trip(id=pk)

    if trip is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            'Trip not found'
        )

    if trip.profile.user.id == user.id:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            'Owner can not join'
        )

    if user.profile.id in {i.id for i in trip.participants}:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            'You already joined'
        )

    await repository.create_participant(
        dict(
            profile_id=user.profile.id,
            trip_id=trip.id
        )
    )

    return Message(msg='Success')
