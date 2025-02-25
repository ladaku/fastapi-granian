from pydantic import BaseModel

class UserType(BaseModel):
    name: str
    username: str
    password: str
    active: bool

class Token(BaseModel):
    access_token: str
    token_type: str