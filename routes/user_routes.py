from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from bson import ObjectId 
from utils.passwordHasser import bcrypted , verify_password 
from utils.jwttoken import create_access_token,create_refresh_token

from db.database import Database 
from utils.auth import get_current_user
from models.user_model import User
from schemas.user_schema import UserSchema

user_router=APIRouter()

user_collection=Database. db.get_collection("users")

@user_router.post("/create", description="create user")
async def create_user(user: User):
    existUser = user_collection.find_one({"email": user.email})
    if existUser is not None:
        return {"message": "User already exists"}
    else:
        passwordHassed = bcrypted(user.password)
        user_object = dict(user)
        user_object["password"] = passwordHassed
        user_object["email"]= user_object["email"].lower()
        newUser = user_collection.insert_one(user_object)
        return {
            "message": "User created",
        }


@user_router.get("/user")
async def get_user_infos(current_userId: str = Depends(get_current_user)):
    users = []
    async for student in user_collection.find():
        users.append(UserSchema(student))
    return users




 # return print(users)
@user_router.post('/login', summary="Create access and refresh tokens for user")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await user_collection.find_one({"email": form_data.username})
    #return print('user-connected',dict(user))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Identifiant ou mot de passe incorrect"
        )

    hashed = user["password"]
    password = form_data.password
    if not verify_password(password, hashed):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
        # Convert ObjectId to string
    user_id = str(user['_id'])

    return {
        "access_token": create_access_token(data={"sub": user_id}),
      "refresh_token": create_refresh_token(user['email']),
    }

