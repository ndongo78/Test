from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel, EmailStr, Field, validator
from bson import ObjectId


class Article(BaseModel):
  title: str
  description: str
  price: float
  image: Optional[
    str]  # Utilisez le type UploadFile pour le champ image
  category_id: str

  @validator('category_id')
  def validate_category_id(cls, value):
    if not ObjectId.is_valid(value):
      raise ValueError('Invalid category_id')
    return value

  class Config:
    schema_extra = {
      "example": {
        "title": "Adidas air max",
        "description": "description de l'article",
        "price": 80,
        "category_id": "id du category"
      }
    }
