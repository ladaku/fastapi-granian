from fastapi import APIRouter, Body, Depends, status
from pydantic import BaseModel
from sqlmodel import Session, select
from typing import Annotated
from nanoid import generate as generate_id
from app.model.post import Post
from app.utils.database import db_session
from sqlalchemy.exc import *
from sqlalchemy import func
import os
import shutil
UPLOAD_DIR = "uploads"  # Ensure this directory exists

class PostController:
    def __init__(self):
        self.current_user = None

    def list(session, page, size):
        total_count = session.exec(select(func.count()).select_from(Post)).one()
        results = session.exec(select(Post).offset(page).limit(size)).all()

        return {"code": status.HTTP_200_OK, "status": True, "message": "created Post", "data": {"data": results, "total": total_count}}
    
    def create(session, video, thumb, title, desc):
        try:
            video_filename = generate_id(size=8) + video.filename
            video_file_path = os.path.join(UPLOAD_DIR, video_filename)
           
            with open(video_file_path, "wb") as buffer:
                shutil.copyfileobj(video.file, buffer)

            thumb_filename = generate_id(size=8) + thumb.filename
            thumb_file_path = os.path.join(UPLOAD_DIR, thumb_filename)
           
            with open(thumb_file_path, "wb") as buffer:
                shutil.copyfileobj(thumb.file, buffer)

            payload_post = Post(title=title, desc=desc, slug=generate_id(size=10), thumb_url=thumb_filename, video_url=video_filename)
            session.add(payload_post)
            session.commit()
            session.refresh(payload_post)
            return {"code": status.HTTP_201_CREATED, "status": True, "message": "created Post", "data": title}
        except IntegrityError:
            session.rollback()
            return {"code": 500, "status": False, "message": "Error iki", "data": None}
            # finally:
            #     db.session.remove()