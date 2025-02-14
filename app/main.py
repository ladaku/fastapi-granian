from typing import Union, Annotated
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Field, SQLModel, Session, create_engine, select
from app.utils.database import engine, db_session
from app.routers.auth import router as router_auth
from app.model.hero import Hero
from app.model.user import User

SessionDep = Annotated[Session, Depends(db_session)]

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    
@app.get("/")
def read_root(session: SessionDep):
    sef = session.exec(select(Hero)).all()
    return {"Hello": "World"}

@app.get("/elite")
def read_root(session: SessionDep):
    sef = session.exec(select(User)).all()
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

app.include_router(router_auth, prefix="/api/v1")