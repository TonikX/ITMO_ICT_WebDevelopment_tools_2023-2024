from typing import List

from fastapi import APIRouter, Depends
from db import get_session
from models import OperationEnum, Operation

operationRouter = APIRouter(prefix="/operations", tags=["operation"])  # отвечает за swagger


@operationRouter.get("/available")
async def get_available():
    return list(OperationEnum)


@operationRouter.get("/", response_model=list[Operation])
async def get_operations(session=Depends(get_session)) -> List[Operation]:
    operations = session.query(Operation).all()
    return operations


@operationRouter.get("/{operation_id}", response_model=Operation)
async def get_operation(operation_id: int, session=Depends(get_session)) -> Operation:
    operation = session.query(Operation).filter_by(id=operation_id).first()
    return operation


@operationRouter.post("/")
async def create_operation(operation: Operation, session=Depends(get_session)):
    operation = Operation.validate(operation)
    if operation.operation not in OperationEnum:
        return "Invalid operation name"
    operation.id = None
    session.add(operation)
    session.commit()
    session.refresh(operation)
    return operation


@operationRouter.patch("/{operation_id}")
async def update_operation(operation: Operation, operation_id: int, session=Depends(get_session)):
    operation = Operation.validate(operation)
    if operation.operation not in OperationEnum:
        return "Invalid operation name"
    operation_from_db = session.query(Operation).filter_by(id=operation_id).first()
    if operation_from_db is None:
        return "No such operation"
    operation_data = operation.model_dump(exclude_unset=True)
    for key, value in operation_data.items():
        setattr(operation_from_db, key, value)
    session.add(operation_from_db)
    session.commit()
    session.refresh(operation_from_db)
    return operation_from_db


@operationRouter.delete("/{operation_name}")
async def delete_operation(operation_name: str, session=Depends(get_session)):
    session.query(Operation).filter(Operation.operation == operation_name).delete()
    session.commit()
    return "Deleted"
