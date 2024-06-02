from typing import List
from fastapi import HTTPException, Depends, APIRouter
from sqlmodel import select
from typing_extensions import TypedDict
from models import Label, LabelDefault
from connection import get_session


router = APIRouter()


@router.get("/")
def labels_list(session=Depends(get_session)) -> List[Label]:
    return session.exec(select(Label)).all()


@router.get("/{label_id}")
def get_label(label_id: int, session=Depends(get_session)) -> Label:
    return session.get(Label, label_id)


@router.post("/")
def label_create(lab: LabelDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                            "data": Label}):
    lab = Label.model_validate(lab)
    session.add(lab)
    session.commit()
    session.refresh(lab)
    return {"status": 200, "data": lab}


@router.delete("/{label_id}")
def delete_label(label_id: int, session=Depends(get_session)) -> TypedDict('Response', {"is_deleted": bool}):
    label = session.get(Label, label_id)
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")
    session.delete(label)
    session.commit()
    return {"is_deleted": True}


@router.patch("/{label_id}")
def update_label(label_id: int, label: LabelDefault, session=Depends(get_session)) -> LabelDefault:
    db_labels = session.get(Label, label_id)
    if not db_labels:
        raise HTTPException(status_code=404, detail="Label not found")
    categories_data = label.model_dump(exclude_unset=True)
    for key, value in categories_data.items():
        setattr(db_labels, key, value)
    session.add(db_labels)
    session.commit()
    session.refresh(db_labels)
    return db_labels
