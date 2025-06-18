from app.model.user import User
from sqlalchemy.inspection import inspect
from sqlalchemy.exc import *
from sqlmodel import select
from fastapi import HTTPException, status
from app.utils.password_lib import hash_password, verify_password
from datetime import datetime, timedelta, timezone
from app.schema.user import Token
import jwt

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
class SignupControl:
    def __new__(self, user, session):
        try:
            print(user)
            user_dict = user.dict()
            hash_pass = hash_password(user_dict["password"])
            user_regist = User(username=user_dict["username"], name=user_dict["name"], password=hash_pass, active=user_dict["active"])
            
            session.add(user_regist)
            session.commit()
            session.refresh(user_regist)
            print(user_regist)
            return {"message": "User registered successfully", "user_id": user_regist.id}
        except IntegrityError as e:
            return HTTPException(status_code=400, detail="username already")
        # try:
        #     print(user["name"], user, 'ju')
        #     return { "error": False, "name": user["name"] }
        # except:
        #     return { "error": True }

    # async def r
    #     try:

    #         return { "error": False }
    #     except:
    #         return { "error": True }

def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
class AuthController:
    def login(user, session):
        try:
            # user_dict = user.dict()
            query = select(User).where(User.username == user.username)
            result = session.exec(query)
            first = result.first()
            if not first:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={ "status": False, "message": "failed Login", "data": None, "error": "Incorrect username or password" },
                    headers={"WWW-Authenticate": "Bearer"},
                )
            verif_pass = verify_password(user.password, first.password)
            print(verif_pass, user.password, first.password, "celeng")
            # if not verif_pass:
            #     raise HTTPException(
            #         status_code=status.HTTP_401_UNAUTHORIZED,
            #         detail={ "status": False, "message": "failed Password", "data": None, "error": "Failed password" },
            #         headers={"WWW-Authenticate": "Bearer"},
            #     )
            
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user.username}, expires_delta=access_token_expires
            )
            
            # for x in result:
            #     print(x, "mmo")
            return { "status": True, "message": "Success Login", "error": None, "data": {"access_token": access_token, "token_type": "bearer"}}
        except NoResultFound as e:
            return { "status": False, "message": "failed Login", "data": None, "error": e }
        
        
    def token(user, session):
        try:
            # user_dict = user.dict()
            query = select(User).where(User.username == user.username)
            result = session.exec(query)
            first = result.first()
            if not first:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={ "status": False, "message": "failed Login", "data": None, "error": "Incorrect username or password" },
                    headers={"WWW-Authenticate": "Bearer"},
                )
            verif_pass = verify_password(user.password, first.password)
            print(verif_pass, user.password, first.password, 'celeng token')
            if not verif_pass:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={ "status": False, "message": "failed Password", "data": None, "error": "Failed password" },
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user.username}, expires_delta=access_token_expires
            )
            
            # for x in result:
            #     print(x, "mmo")
            return Token(access_token=access_token, token_type="bearer")
        except NoResultFound as e:
            return { "status": False, "message": "failed Login", "data": None, "error": e }