from fastapi import APIRouter, HTTPException, status, Depends

from models.category import Category 
from db.database import Database 
from schemas.category_schema import CategorySchema


category_router =APIRouter()

category_collection =Database.db.get_collection("category")


@category_router.get("/")
async def get_categories():
    categories= []
    async for category in category_collection.find():
        categories.append(CategorySchema(category))
    return categories

@category_router.post("/create")
async def create_category(newcategory:Category): 
    category_dict= newcategory.dict()
    newItem= await category_collection.insert_one(category_dict)

    return newItem
 


        


        

