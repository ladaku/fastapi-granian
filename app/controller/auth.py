from app.model.user import User
from sqlalchemy.inspection import inspect
from sqlalchemy.exc import *
from fastapi import HTTPException
class SignupControl:
    def __new__(self, user, session):
        try:
            print(user)
        #  jnv = **user.dict()
            user_test = User(**user.dict())
            if inspect(user_test):
                print("NOt")
            else:
                print("notttt")
            session.add(user_test)
            session.commit()
            session.refresh(user_test)
            lop = { "data": user.dict() }
            print(user_test)
            return lop
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
        