from sqlmodel import SQLModel, Field, Relationship


class ReviewBase(SQLModel):
    trip_id: int = Field(foreign_key='trip.id')
    rate: int
    comment: str | None


class Review(ReviewBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='user.id')
    user: 'User' = Relationship(back_populates='reviews')
