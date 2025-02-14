from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel
from sqlmodel import Session
from typing import Annotated
from app.utils.database import db_session
from app.controller.auth import SignupControl


SessionDep = Annotated[Session, Depends(db_session)]
class UserType(BaseModel):
    name: str
    username: str
    password: str
    active: bool

router = APIRouter(tags=["auth"])

@router.post("/auth/signup")
async def signup(user: Annotated[UserType, Body(embed=True)], session: SessionDep):
    return SignupControl(user, session)