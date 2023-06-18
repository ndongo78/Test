from pydantic import BaseModel, EmailStr, Field, validator

import re

class Category(BaseModel):
    name: str
    
    class Config:
        schema_extra={
          "exemple":{
               "name":"Chaussures"
          }
        }
    @validator('name')
    def nameValidator(cls, v):
        valid = re.compile('^([a-zA-Z ])+$')
        if valid.match(v) is None or len(v) < 3:
            raise ValueError('Category est invalid')
        if v == "":
            raise ValueError('Category est required')
        return v.title() 
    
    


