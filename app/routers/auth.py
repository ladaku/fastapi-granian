from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel
from sqlmodel import Session
from typing import Annotated
from app.utils.database import db_session
from app.controller.auth import SignupControl, AuthController
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

SessionDep = Annotated[Session, Depends(db_session)]
class UserType(BaseModel):
    name: str
    username: str
    password: str
    active: bool

class SigninType(BaseModel):
    username: str
    password: str

router = APIRouter(tags=["auth"])

@router.post("/auth/signup")
async def signup(user: Annotated[UserType, Body(embed=True)], session: SessionDep):
    return SignupControl(user, session)

@router.post("/auth/signin")
async def signin(user: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    return AuthController.login(user, session)
