from fastapi import FastAPI 
from motor.motor_asyncio import AsyncIOMotorClient

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from bson import ObjectId 
from passwordHasser import bcrypted , verify_password 
from jwttoken import create_access_token,create_refresh_token

from models import User


from auth import get_current_user

from schemas import UserSchema

client = AsyncIOMotorClient('mongodb+srv://ndongo:a9125844@cluster0.ixyfun2.mongodb.net/test?retryWrites=true&w=majority')

db=client.Cluster0
user_collection=db.get_collection("users")

app=FastAPI()

@app.get("/")
def root():
  return {"message":"hello world "}

@app.get("/user")
async def get_user_infos(current_userId: str = Depends(get_current_user)):
    users = []
    async for student in user_collection.find():
        users.append(UserSchema(student))
    return users




 # return print(users)
@app.post('/login', summary="Create access and refresh tokens for user")
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

