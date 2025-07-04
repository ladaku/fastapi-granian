from typing import Union, Annotated
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, SQLModel, Session, create_engine, select
from app.utils.database import engine, db_session
from app.routers.auth import router as router_auth
from app.routers.post import router as router_post
from app.routers.tag import router as router_tag
from app.controller.auth import AuthController
from dotenv import load_dotenv, find_dotenv
import os
from app.model.hero import Hero
from app.model.user import User
from app.model.post import Post, Tag, PostTagLink

load_dotenv(find_dotenv())

SessionDep = Annotated[Session, Depends(db_session)]

app = FastAPI()

# Allow all origins (not recommended for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

FASTAPI_ENVIRONTMENT = os.getenv("FASTAPI_ENVIRONTMENT")
static_directory = "/var/www/malware-bkp" if FASTAPI_ENVIRONTMENT == "production" else "uploads"
app.mount("/static", StaticFiles(directory=static_directory), name="static")
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    
@app.get("/")
def read_root(session: SessionDep):
    sef = session.exec(select(Hero)).all()
   # post = session.exec(select())
    return {"Hello": "World" }

@app.post("/token")
async def signin(user: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    return AuthController.token(user, session)


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

app.include_router(router_auth, prefix="/api/v1")
app.include_router(router_post, prefix="/api/v1")
app.include_router(router_tag, prefix="/api/v1")