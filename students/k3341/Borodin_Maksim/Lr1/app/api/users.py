from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.api.deps import get_current_user
from app.core.security import hash_password, verify_password
from app.db.session import get_session
from app.models.user import User
from app.schemas.user import PasswordChangeRequest, UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserRead])
def list_users(
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
) -> list[UserRead]:
    users = session.exec(select(User)).all()
    return [UserRead.model_validate(user) for user in users]


@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)) -> UserRead:
    return UserRead.model_validate(current_user)


@router.patch("/me/password")
def change_password(
    payload: PasswordChangeRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> dict[str, bool]:
    if not verify_password(payload.old_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Old password is incorrect")
    current_user.password_hash = hash_password(payload.new_password)
    session.add(current_user)
    session.commit()
    return {"ok": True}
