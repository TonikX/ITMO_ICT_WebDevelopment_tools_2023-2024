from pydantic import BaseModel, model_validator


class UserLogin(BaseModel):
    username: str
    password: str


class ChangePasswordSchema(BaseModel):
    password: str
    new_password: str

    @model_validator(mode='after')
    def check_passwords_match(self, new_password: str) -> 'ChangePasswordSchema':
        if self.password is not None and new_password is not None and self.password == new_password:
            raise ValueError('passwords do not match')
        return self

