from fastapi import APIRouter
from pydantic import BaseModel
from app.controller.auth import SignupControl
class UserType(BaseModel):
    name: str
    username: str
    password: str

router = APIRouter(tags=["auth"])

@router.post("/auth/signup")
async def signup(user: UserType):
    return SignupControl(user)