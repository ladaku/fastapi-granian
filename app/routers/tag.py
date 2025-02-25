from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel
from sqlmodel import Session
from app.schema.user import UserType
from app.schema.tag import TagType
from app.model.post import Tag
from typing import Annotated
from app.utils.database import db_session
from app.utils.middleware import get_current_user
from app.controller.tag import TagContoller

SessionDep = Annotated[Session, Depends(db_session)]

router = APIRouter(tags=["tag"])

@router.get("/tag")
async def list_tag(current_user: Annotated[UserType, Depends(get_current_user)], session: SessionDep):
    return TagContoller.list(session)

@router.post("/tag")
async def add_tag(current_user: Annotated[UserType, Depends(get_current_user)], tag: Annotated[Tag, Body(embed=True)],session: SessionDep):
    return TagContoller.create(session, tag)