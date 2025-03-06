from fastapi import APIRouter, Body, Depends, UploadFile, File, Form, Query
from pydantic import BaseModel
from sqlmodel import Session
from app.schema.user import UserType
from app.schema.post import PostPayload
from typing import Annotated
from app.utils.database import db_session
from app.utils.middleware import get_current_user
from app.controller.post import PostController

SessionDep = Annotated[Session, Depends(db_session)]

router = APIRouter(tags=["post"])

@router.get("/posts/")
async def list_post(current_user: Annotated[UserType, Depends(get_current_user)], session: SessionDep, page: int = 0, size: int = Query(default=100, le=100)):
    return PostController.list(session, page, size)

@router.post("/posts")
async def create_post(current_user: Annotated[UserType, Depends(get_current_user)], session: SessionDep, video: Annotated[UploadFile, File()], thumb: Annotated[UploadFile, File()], title: Annotated[str, Form()], desc: Annotated[str, Form()]):
    print(video.filename)
    return PostController.create(session, video, thumb, title, desc)