# Сервис для работы со скиллами

```python
from fastapi import APIRouter, Depends, HTTPException
from typing_extensions import TypedDict, List
from sqlmodel import select

import sys
sys.path.append("../..")

from lab1.TeamTinder.connection import get_session
from lab1.TeamTinder.models import *


router = APIRouter()


@router.post("/skill")
def skill_create(skill: SkillDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Skill}):
    skill = Skill.model_validate(skill)
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return {"status": 200, "data": skill}


@router.get("/skill/list", response_model=List[SkillExtended])
def skill_list(session=Depends(get_session)) -> List[Skill]:
    return session.exec(select(Skill)).all()


@router.get("/skill/{skill_id}", response_model=SkillExtended)
def skill_read(skill_id: int, session=Depends(get_session)) -> Skill:
    return session.get(Skill, skill_id)
```
