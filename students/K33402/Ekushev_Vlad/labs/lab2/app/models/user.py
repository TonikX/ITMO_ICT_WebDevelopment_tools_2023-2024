from fastapi.exceptions import HTTPException
from pydantic import Field, validator
from starlette import status
from core.errors import API_ERRORS
from core.utils import slugify
from pydantic import BaseModel


class UserUsername(BaseModel):
    username: str = Field(max_length=50)

    @validator("username")
    def checkUsername(self, username):
        if len(slugify(username)) < 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=API_ERRORS["username.TooShort"],
            )
        return username


class UserPassword(BaseModel):
    password: str = Field(max_length=50)

    @validator("password")
    def checkPassword(self, password):
        if len(password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=API_ERRORS["password.InvalidLength"],
            )
        return password


class UserContacts(BaseModel):
    email: str = Field(default="", max_length=50)
    telegram: str = Field(default="", max_length=50)
    website: str = Field(default="", max_length=50)


class UserBase(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    lastname: str = Field(min_length=2, max_length=50)
    contact: UserContacts = Field(default=UserContacts())
    gender: bool = Field(default=False)
    birthDate: str = Field(default="")
    location: str = Field(default="")
    information: str = Field(default="", max_length=1200)
    avatarUrl: str = Field(default="")
    coverUrl: str = Field(default="")


class UserInDB(BaseModelWithId, UserBase):
    passwordHash: str = Field(default="")

    class Config(BaseModelWithIdConfig):
        exclude = {"password"}

        schema_extra = {
            "example": {
                "username": "My goodName",
                "name": "MyName",
                "lastname": "MyLastname",
                "contact": {
                    "email": "MyEmail",
                    "telegram": "MyTelegram",
                    "website": "MyWebsite",
                },
                "gender": 0,
                "birthDate": "13.12.1337",
                "passwordHash": "adhahduad123u1",
                "location": "MyLocation",
                "information": "MyInformation",
                "skillTags": [{"label": "ReactJS"}],
                "avatarUrl": "/media/avatars/adwada.jpg",
                "coverUrl": "/media/avatars/akdlakldklakl.jpeg",
            }
        }



# User Login POST (/api/user/login)
class UserLoginReq(UserUsername, UserPassword):
    fingerPrint: str = Field(...)


class UserLoginRes(MyBaseModelWithExcAndInc):
    accessToken: str = Field(...)
    refreshToken: str = Field(...)
    expires: int = Field(...)


# User Register POST (/api/user/register)
class UserRegisterReq(UserBase, UserPassword):
    pass


class UserRegisterRes(UserBase):
    pass


# User Me POST (/api/user/me)


class UserSelfChangeReq(UserBase):
    class Config:
        exclude = {"username", "avatarUrl", "coverUrl"}



class UserSelfChangeRes(UserBase):
    pass


# User Info GET (/api/user/<username>)


class UserInfoRes(UserBase):
    pass


# User List Suitable POST (/api/user/list_suitable)
class UserListSuitableRes(UserBase):
    pass
