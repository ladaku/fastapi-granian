from fastapi import APIRouter, Body, Depends, UploadFile, File
from pydantic import BaseModel
from sqlmodel import Session
from app.schema.user import UserType
from typing import Annotated
from app.utils.database import db_session
from app.utils.middleware import get_current_user
from app.controller.post import PostController

SessionDep = Annotated[Session, Depends(db_session)]

router = APIRouter(tags=["post"])

@router.get("/posts")
async def list_post(current_user: Annotated[UserType, Depends(get_current_user)], session: SessionDep):
    return "mekk"

@router.post("/posts")
async def create_post(current_user: Annotated[UserType, Depends(get_current_user)], session: SessionDep, video: Annotated[UploadFile, File()]):
    print(video.filename)
    return PostController.create(session, video)