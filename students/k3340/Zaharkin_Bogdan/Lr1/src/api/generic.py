# Response annotation for API
from typing import Generic, Type, TypeVar, TypedDict
from fastapi import HTTPException
from sqlmodel import SQLModel, Session, select


# Define types for Generic
InputModel = TypeVar('InputModel', bound=SQLModel)
OutputModel = TypeVar('OutputModel', bound=SQLModel)

# Response annotation for API
class Response(TypedDict, Generic[OutputModel]):
    status: int
    data: OutputModel


# Generic function for creation object and addition in database
def create_object(session: Session, input_model: InputModel, output_model: Type[OutputModel]) -> Response[OutputModel]:
    output_instance = output_model.model_validate(input_model)
    session.add(output_instance)
    session.commit()
    session.refresh(output_instance)
    return {"status": 201, "data": output_instance}

# Generic function for read all objects from database
def read_object_list(session: Session, output_model: Type[OutputModel]) -> list[OutputModel]:
    return session.exec(select(output_model)).all()

# Generic function for read object by id from database
def read_object(session: Session, id: int, output_model: Type[OutputModel]) -> OutputModel:
    output_instance = session.get(output_model, id)
    if not output_instance:
        raise HTTPException(status_code=404, detail=f"{output_model.__name__} not found")
    return output_instance

# Generic function for update object by id from database
def update_object(session: Session, id: int, input_model: InputModel, output_model: Type[OutputModel]) -> InputModel:
    output_instance = session.get(output_model, id)
    if not output_instance:
        raise HTTPException(status_code=404, detail=f"{output_model.__name__} not found")
    output_data = input_model.model_dump(exclude_unset=True)
    for key, value in output_data.items():
        setattr(output_instance, key, value)
    session.add(output_instance)
    session.commit()
    session.refresh(output_instance)
    return output_instance

# Generic function for delete object by id from database
def delete_object(session: Session, id: int, output_model: Type[OutputModel]) -> dict:
    output_instance = session.get(output_model, id)
    if not output_instance:
        raise HTTPException(status_code=404, detail=f"{output_model.__name__} not found")
    session.delete(output_instance)
    session.commit()
    return {"ok": True}
