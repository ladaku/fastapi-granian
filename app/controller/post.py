from fastapi import APIRouter, Body, Depends, status
from pydantic import BaseModel
from sqlmodel import Session, select
from typing import Annotated
from nanoid import generate as generate_id
from app.model.post import Post, PostTagLink
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

        return {"code": status.HTTP_200_OK, "status": True, "message": "success getting Post", "data": {"data": results, "total": total_count}}
    
    def create(session, video, thumb, title, desc, tags):
        try:
            video_filename = generate_id(size=8) + video.filename
            video_file_path = os.path.join(UPLOAD_DIR, video_filename)
            print(tags[0].split(','), 'pentil')
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

            tags = tags[0].split(',')
            payload_tags = []
            print(type(payload_post.id), payload_post, "erick")
            for x in tags:
                if isinstance(int(x), (int, float, complex)):
                    payload_tags.append(
                        PostTagLink(post_id=payload_post.id, tag_id=int(x))
                    )
            session.add_all(payload_tags)
            session.commit()
            #session.refresh(payload_tags)
            return {"code": status.HTTP_201_CREATED, "status": True, "message": "created Post", "data": payload_post.id}
        except IntegrityError as e:
            session.rollback()
            return {"code": 500, "status": False, "message": "Error iki", "data": e}
            # finally:
            #     db.session.remove()

    def remove(session, id):
        try:
            query = select(Post).where(Post.id == id)
            result = session.exec(query)
            post = result.one()
            
            video_file_path = os.path.join(UPLOAD_DIR, post.video_url)
            thumb_file_path = os.path.join(UPLOAD_DIR, post.thumb_url)

            if os.path.exists(video_file_path):
                print("vid url ada")
                os.remove(video_file_path)
            if os.path.exists(thumb_file_path):
                print("thumb url ada")
                os.remove(thumb_file_path)
            
            session.delete(post)
            session.commit()
            return {"code": status.HTTP_200_OK, "status": True, "message": "Success remove Post", "data": post.id}
        except IntegrityError:
            return {"code": status.HTTP_400_BAD_REQUEST, "status": False, "message": "Failed remove Post", "data": None}
        
    def detail(session, slug):
        try:
            query = select(Post).where(Post.slug == slug)
            result = session.exec(query)
            post = result.one()
            
            # video_file_path = os.path.join(UPLOAD_DIR, post.video_url)
            # thumb_file_path = os.path.join(UPLOAD_DIR, post.thumb_url)

            # if os.path.exists(video_file_path):
            #     print("vid url ada")
            #     os.remove(video_file_path)
            # if os.path.exists(thumb_file_path):
            #     print("thumb url ada")
            #     os.remove(thumb_file_path)
            
            # session.delete(post)
            # session.commit()
            return {"code": status.HTTP_200_OK, "status": True, "message": "Success remove Post", "data": post}
        except IntegrityError:
            return {"code": status.HTTP_400_BAD_REQUEST, "status": False, "message": "Failed remove Post", "data": None}
        