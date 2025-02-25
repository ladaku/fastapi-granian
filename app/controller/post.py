from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel
from sqlmodel import Session
from typing import Annotated
from app.utils.database import db_session
import os
import shutil
UPLOAD_DIR = "uploads"  # Ensure this directory exists

class PostController:
    def __init__(self):
        self.current_user = None

    async def list():
        return "guguk"
    
    def create(session, video):
        print(video, "aff")
        file_path = os.path.join(UPLOAD_DIR, video.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)
        return { "ast": "num"}