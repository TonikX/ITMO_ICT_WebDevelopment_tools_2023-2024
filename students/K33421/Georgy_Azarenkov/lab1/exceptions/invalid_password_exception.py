from fastapi import HTTPException


class InvalidPasswordException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Invalid password")

