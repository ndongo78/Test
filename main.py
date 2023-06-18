from fastapi import FastAPI 
from db.database import Database 
from fastapi.staticfiles import StaticFiles

from routes.user_routes import user_router
from routes.category_routes import category_router
from routes.article_routes import article_router

app=FastAPI()
app.on_event("startup")
Database()


app.mount("/images", StaticFiles(directory="images"), name="images")
@app.get("/")
def root():
  return {"message":"hello world "}

app.include_router(user_router, tags=["users"], prefix="/api/users")
app.include_router(category_router, tags=["category"], prefix="/api/categories")
app.include_router(article_router, tags=["article"], prefix="/api/article")