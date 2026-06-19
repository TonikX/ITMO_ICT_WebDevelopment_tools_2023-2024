"""Дополнительные API-методы по пользователям (п.5 задания на 15 баллов).

- получение информации о пользователе;
- получение списка пользователей;
- смена пароля;
- (бонус) подтверждение регистрации участника организатором.
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, require_role
from app.models import User, UserRole
from app.schemas import MessageOut, PasswordChange, UserOut
from app.security import hash_password, verify_password

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.get("", response_model=List[UserOut])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Список пользователей (с пагинацией). Требует аутентификации."""
    return db.query(User).offset(skip).limit(limit).all()


@router.put("/me/password", response_model=MessageOut)
def change_password(
    data: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Смена пароля текущего пользователя."""
    if not verify_password(data.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Старый пароль указан неверно",
        )
    current_user.hashed_password = hash_password(data.new_password)
    db.commit()
    return MessageOut(detail="Пароль успешно изменён")


@router.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Информация о конкретном пользователе по id."""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    return user


@router.post("/{user_id}/confirm", response_model=UserOut)
def confirm_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.organizer)),
):
    """Подтверждение регистрации участника организатором."""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    user.is_confirmed = True
    db.commit()
    db.refresh(user)
    return user
