from typing import Sequence, Type

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from auth import AuthHandler
from connection import get_session
from models.transport_model import Transport, TransportDefault

transport_router = APIRouter(tags=['Transport'])
auth_handler = AuthHandler()


@transport_router.get("/transport/all")
def get_all_transports(session: Session = Depends(get_session)) -> Sequence[Transport]:
    transports = session.exec(select(Transport)).all()
    return transports


@transport_router.post("/transport/create")
def create_transport(transport: TransportDefault, session: Session = Depends(get_session)) -> Transport:
    transport = Transport.model_validate(transport)
    session.add(transport)
    session.commit()
    session.refresh(transport)
    return transport

@transport_router.delete("/transport/delete")
def delete_transport(transport: TransportDefault, session: Session = Depends(get_session)):
    transport = Transport.model_validate(transport)
    session.delete(transport)
    session.commit()
    return transport
