from typing import List

from fastapi import APIRouter, Depends, HTTPException
from db import get_session
from models.operations import Operation

operationRouter = APIRouter(prefix="", tags=["operation"])  # отвечает за swagger


@operationRouter.get("/operations/", response_model=list[Operation])
async def get_operations(session=Depends(get_session)) -> List[Operation]:
    operations = session.query(Operation).all()
    return operations


@operationRouter.get("/operations/{operation_id}", response_model=Operation)
async def get_operation(operation_id: int, session=Depends(get_session)) -> Operation:
    operation = session.query(Operation).filter_by(id=operation_id).first()
    return operation


@operationRouter.post("/operations/")
async def create_operation(operation: Operation, session=Depends(get_session)):
    operation = Operation.validate(operation)
    operation.id = None
    session.add(operation)
    session.commit()
    session.refresh(operation)
    return operation


@operationRouter.patch("/operations/{operation_id}")
async def update_operation(operation: Operation, operation_id: int, session=Depends(get_session)):
    operation = Operation.validate(operation)
    operation_from_db = session.query(Operation).filter_by(id=operation_id).first()
    if operation_from_db is None:
        raise HTTPException(status_code=404, detail="No such operation")
    operation_data = operation.model_dump(exclude_unset=True)
    for key, value in operation_data.items():
        setattr(operation_from_db, key, value)
    session.add(operation_from_db)
    session.commit()
    session.refresh(operation_from_db)
    return operation_from_db


@operationRouter.delete("/operations/{operation_id}")
async def delete_operation(operation_id: int, session=Depends(get_session)):
    session.query(Operation).filter_by(id=operation_id).delete()
    session.commit()
    return "Deleted"
