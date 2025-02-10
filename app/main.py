from typing import Union, Annotated
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Field, SQLModel, Session, create_engine, select

from app.routers.auth import router as router_auth

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str

DATABASE_URL = "postgresql://adminer:asdasd21@103.150.93.114:5432/bkp_new"
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    
@app.get("/")
def read_root(session: SessionDep):
    sef = session.exec(select(Hero)).all()
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

app.include_router(router_auth, prefix="/api/v1")