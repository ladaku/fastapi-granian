from app.model.user import User
from sqlalchemy.inspection import inspect
from sqlalchemy.exc import *
from fastapi import HTTPException
from app.utils.password_lib import hash_password
class SignupControl:
    def __new__(self, user, session):
        try:
            print(user)
            user_dict = user.dict()
            hash_pass = hash_password(user_dict["username"])
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
        