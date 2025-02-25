from sqlmodel import select
from app.model.post import Tag

class TagContoller:
    def __init__(self):
        self.opo = 'opo'

    def list(session):
        query = session.exec(select(Tag))
        result = query.all()
        return result
    
    def create(session, tag):
        print(tag, "tuan")
        session.add(tag)
        session.commit()
        session.refresh(tag)
        return '7888'