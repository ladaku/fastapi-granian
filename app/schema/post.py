from pydantic import BaseModel

class PostPayload(BaseModel):
    title: str
    desc: str 
    slug: str