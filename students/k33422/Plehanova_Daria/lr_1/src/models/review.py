from sqlmodel import SQLModel, Field, Relationship

from .user import UserBaseId


class ReviewBase(SQLModel):
    trip_id: int = Field(foreign_key='trip.id')
    rate: int
    comment: str | None


class ReviewScheme(SQLModel):
    rate: int
    comment: str = ''


class ReviewBaseId(ReviewBase):
    id: int


class ReviewBaseList(ReviewBaseId):
    user_id: int


class ReviewBaseDetail(ReviewBaseId):
    user: UserBaseId

class Review(ReviewBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='user.id')
    user: 'User' = Relationship(back_populates='reviews')
