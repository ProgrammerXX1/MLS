from pydantic import BaseModel

class UserRegister(BaseModel):
    username: str
    password: str
    is_api_user: bool = False

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
