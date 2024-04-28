from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    """Strict readonly"""

    id: int
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False

    model_config = ConfigDict(
        frozen=True,
        strict=True,
        from_attributes=True
    )
