from fastapi import HTTPException


class Forbidden(HTTPException):
    def __init__(self):
        super().__init__(status_code=403, detail="Forbidden action")

