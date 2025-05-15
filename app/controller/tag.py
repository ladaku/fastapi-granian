from sqlmodel import select
from app.model.post import Tag
from fastapi import status
from sqlalchemy.exc import *
from sqlalchemy import func
class TagContoller:
    def __init__(self):
        self.opo = 'opo'

    def list(session):
        query = session.exec(select(Tag))
        result = query.all()
        return result
    
    def tag_pagination(session, page, size):
        total_count = session.exec(select(func.count()).select_from(Tag)).one()
        results = session.exec(select(Tag).offset(page).limit(size)).all()

        return {"code": status.HTTP_200_OK, "status": True, "message": "success getting Post", "data": {"data": results, "total": total_count}}
    
    def create(session, tag):
        try:
            new = Tag(name=tag.name)
            session.add(new)
            session.commit()
            session.refresh(new)
            return {"code": status.HTTP_201_CREATED, "status": True, "message": "Success created tag", "data": None}
        except IntegrityError:
            return {"code": status.HTTP_400_BAD_REQUEST, "status": False, "message": "Failed created tag", "data": None}