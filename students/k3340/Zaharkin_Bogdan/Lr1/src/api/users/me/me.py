from fastapi import HTTPException
from sqlmodel import Session, select

from src.api.generic import Response
from src.api.users.me.default import UserCreate, UserLogin
from src.api.users.me.schemas import UserJWTResponse, UserResponse
from src.auth.auth import create_access_token, get_password_hash, verify_password
from src.db.models import User

# Function for getting an item from the database by username
def get_user_by_username(username: str, session: Session) -> User:
    statement = select(User).where(User.username == username)
    result = session.exec(statement)
    user = result.first()

    return user

# Function for verify password by username
def verify_password_by_username(password: str, username: str, session: Session) -> bool:
    user = get_user_by_username(username, session)

    if not user:
        return False

    return verify_password(password, user.password_hash)

# Function for creation user and addition in database
def create_user(user_data: UserCreate, session: Session) -> Response[UserJWTResponse]:
        user_data_dict = user_data.model_dump()

        if get_user_by_username(user_data_dict["username"], session):
            raise HTTPException(
                status_code=409,
                detail="The user already exists"
                )

        new_user = User(**user_data_dict)
        new_user.password_hash = get_password_hash(user_data_dict["password"])

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        user_response = UserJWTResponse(**user_data_dict,
                                        access_token=None)

        return {"status": 201, "data": user_response}

# Function for resetting password for user
def reset_password_user(user_data: UserLogin, session: Session) -> Response[UserJWTResponse]:
        user_data_dict = user_data.model_dump()

        user = get_user_by_username(user_data_dict["username"], session)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="Not found"
                )
        
        output_instance = session.get(User, user.id)
        output_instance.password_hash = get_password_hash(user_data_dict["password"])
        session.add(output_instance)
        session.commit()
        session.refresh(user)

        user_dict = user.model_dump()

        user_response = UserJWTResponse(**user_dict,
                                        access_token=None,
                                        password=user_data_dict["password"])

        return {"status": 201, "data": user_response}

# Function for login user and creating access token
def enter_into_user(user_data: UserLogin, session: Session) -> Response[UserJWTResponse]:
        user_data_dict = user_data.model_dump()

        user = get_user_by_username(user_data_dict["username"], session)

        if not user or not verify_password_by_username(user_data_dict["password"], user_data_dict["username"], session):
            raise HTTPException(
                status_code=401,
                detail="Not authorized"
                )

        access_token = create_access_token(data=user.username)

        user_dict = user.model_dump()
        user_response = UserJWTResponse(**user_dict, 
                                        access_token=access_token,
                                        password=user_data_dict["password"])
        
        return {"status": 201, "data": user_response}

# Function for getting information about current user
def info_user(username: str, session: Session) -> Response[UserResponse]:
    user = get_user_by_username(username, session)
    user_data_dict = user.model_dump()
    user_response = UserResponse(**user_data_dict)

    return {"status": 200, "data": user_response}
