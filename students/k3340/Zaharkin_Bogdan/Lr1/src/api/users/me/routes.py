from fastapi import APIRouter, Depends

from src.auth.dependencies import AccessTokenBearer
from src.api.generic import Response
from src.api.users.me.default import UserCreate, UserLogin
from src.api.users.me.me import create_user, enter_into_user, info_user, reset_password_user
from src.api.users.me.schemas import UserJWTResponse, UserResponse
from src.db.connection import get_session


router = APIRouter(prefix="/me", tags=["me"])

# Auth for User
@router.post("/register")
def register_user(user: UserCreate, session=Depends(get_session)) -> Response[UserJWTResponse]:
    """
    Register a user.
    
    - **user**: UserCreate object containing user creation details.
    - **session**: Database session dependency.

    Returns:
        Response[UserJWTResponse]: The user response with optional access token.
    """    
    return create_user(user, session)

@router.post("/login")
def login_user(user: UserLogin, session=Depends(get_session)) -> Response[UserJWTResponse]:
    """
    Login user.
    
    - **user**: UserLogin object containing user login details.
    - **session**: Database session dependency.

    Returns:
        Response[UserJWTResponse]: The user response with optional access token
    """    
    return enter_into_user(user, session)

@router.post("/password")
def password_user(user: UserLogin, session=Depends(get_session)) -> Response[UserJWTResponse]:
    """
    Reset password user.
    
    - **user**: UserLogin object containing user login details.
    - **session**: Database session dependency.

    Returns:
        Response[UserJWTResponse]: The user response with optional access token
    """     
    return reset_password_user(user, session)

@router.get("/")
def get_info_current_user(token=Depends(AccessTokenBearer()), session=Depends(get_session)) -> Response[UserResponse]:
    """
    Get information about current user.
    
    - **token**: Access token dependency.
    - **session**: Database session dependency.

    Returns:
        Response[UserResponse]: The user response
    """   
    return info_user(token['sub'], session)
