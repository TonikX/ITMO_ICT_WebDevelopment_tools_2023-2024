from typing import Union
from sqlmodel import Session, select
from src.models import ExchangeRequest, ExchangeRequestUpdateStatus

# from typing import Union


def get_exchange_request_by_id(
    session: Session, id: int
) -> Union[ExchangeRequest, None]:
    statement = select(ExchangeRequest).where(ExchangeRequest.id == id)
    exchange_request = session.exec(statement).first()
    return exchange_request


def create_exchange_request(
    session: Session, sender_id: int, receiver_id: int, book_ownership_id: int
) -> ExchangeRequest:
    exchange_request = ExchangeRequest(
        sender_id=sender_id,
        receiver_id=receiver_id,
        book_ownership_id=book_ownership_id,
    )
    session.add(exchange_request)
    session.commit()
    session.refresh(exchange_request)
    return exchange_request


def update_exchange_request(
    session: Session, id: int, state_update: ExchangeRequestUpdateStatus
) -> Union[ExchangeRequest, None]:
    exchange_request = get_exchange_request_by_id(session, id)
    if not exchange_request:
        return None

    exchange_request.status = state_update.status or exchange_request.status
    exchange_request.received = state_update.received or exchange_request.received
    exchange_request.sent = state_update.sent or exchange_request.sent
    session.add(exchange_request)
    session.commit()
    session.refresh(exchange_request)
    return exchange_request
