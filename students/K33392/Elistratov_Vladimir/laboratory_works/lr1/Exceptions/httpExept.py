from fastapi import HTTPException
from starlette import status

unauthorizedException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

usernameAlreadyExistedException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Username already existed",
)

incorrectPasswordException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Incorrect old password",
)

alreadyRegisteredOnTravelException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="You already registered on this travel",
)

transportNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Transport not found",
)

travelNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Travel not found",
)

applicationNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Application not found",
)

userNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found",
)

travelPathNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="TravelPath not found",
)

goOutOfThereException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="GO OUT OF THERE",
)

travelLeaderApplicationException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="You are lead this travel",
)