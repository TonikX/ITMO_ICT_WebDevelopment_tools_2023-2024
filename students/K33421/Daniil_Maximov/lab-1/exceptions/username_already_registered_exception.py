from fastapi import HTTPException


class UsernameAlreadyRegisteredException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Username already registered")
