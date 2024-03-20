from fastapi import APIRouter, HTTPException
from fastapi import Depends
from src.models import (
    User,
    ExchangeRequestCreate,
    ExchangeRequest,
    ExchangeRequestUpdateStatus,
    ExchangeRequestStatus,
)
from src.config import db
from src.services import (
    auth as auth_service,
    exchange_requests as exchange_request_service,
)
from sqlmodel import Session

router = APIRouter()


@router.post("/")
def create_exchange_request(
    exchange_create: ExchangeRequestCreate,
    session: Session = Depends(db.get_session),
    current_user: User = Depends(auth_service.get_current_user),
) -> ExchangeRequest:
    new_exchange_request = exchange_request_service.create_exchange_request(
        session=session,
        sender_id=current_user.id,
        book_ownership_id=exchange_create.book_ownership_id,
        receiver_id=exchange_create.receiver_id,
    )
    return new_exchange_request


@router.put("/{exchange_request_id}")
def update_exchange_request_status(
    exchange_request_id: int,
    status_update: ExchangeRequestUpdateStatus,
    session: Session = Depends(db.get_session),
    current_user: User = Depends(auth_service.get_current_user),
) -> ExchangeRequest:
    exchange_request = exchange_request_service.get_exchange_request_by_id(
        session=session, id=exchange_request_id
    )
    if not exchange_request:
        raise HTTPException(status_code=404, detail="Book not found")

    if exchange_request.status == ExchangeRequestStatus.pending:
        if exchange_request.receiver_id != current_user.id:
            raise HTTPException(status_code=404, detail="Can not update")
        return exchange_request_service.update_exchange_request(
            session=session,
            id=exchange_request_id,
            state_update=ExchangeRequestUpdateStatus(status=status_update.status),
        )  # type: ignore

    if exchange_request.status == ExchangeRequestStatus.declined:
        raise HTTPException(status_code=404, detail="Can not update")

    if exchange_request.sender_id == current_user.id and not exchange_request.sent:
        return exchange_request_service.update_exchange_request(
            session=session,
            id=exchange_request_id,
            state_update=ExchangeRequestUpdateStatus(sent=status_update.sent),
        )  # type: ignore

    if (
        exchange_request.receiver_id == current_user.id
        and exchange_request.sent
        and not exchange_request.received
    ):
        return exchange_request_service.update_exchange_request(
            session=session,
            id=exchange_request_id,
            state_update=ExchangeRequestUpdateStatus(received=status_update.received),
        )  # type: ignore

    raise HTTPException(status_code=404, detail="Can not update")
