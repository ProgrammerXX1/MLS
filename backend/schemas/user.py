from pydantic import BaseModel,Field

class UserRegister(BaseModel):
    username: str = Field(min_length=1)
    password: str
    is_api_user: bool = False

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
