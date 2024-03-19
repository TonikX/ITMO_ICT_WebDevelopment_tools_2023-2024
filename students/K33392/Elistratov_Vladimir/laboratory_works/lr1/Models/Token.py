from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Token(SQLModel):
    access_token: str
    token_type: str