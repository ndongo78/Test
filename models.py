from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
import re


class User(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr = Field(..., normalize_email=True)
    password: str
    phone: str
    address: str

    class Config:
        schema_extra = {
            "example": {
                "firstname": "John",
                "lastname": "Doe",
                "email": "johndoe@example.com",
                "password": "mypassword",
                "phone": 1234567890,
                "address": "123 Main Street",
            }
        }

    @validator('firstname')
    def nameValidator(cls, v):
        valid = re.compile('^([a-zA-Z ])+$')
        if valid.match(v) is None or len(v) < 3:
            raise ValueError('Prenom est invalid')
        if v == "":
            raise ValueError('Prenom est required')
        return v.title()

    # lastname validation
    @validator('lastname')
    def lastnameValidator(cls, v):
        valid = re.compile('^([a-zA-Z ])+$')
        if valid.match(v) is None or len(v) < 3:
            raise ValueError('lastname est invalid')
        if v == "":
            raise ValueError('lastname est required')
        return v.title()

    # phone validation
    @validator('phone')
    def phoneValidator(cls, v):
        valid = re.compile('^([0-9])+$')
        if valid.match(v) is None or len(v) < 3:
            raise ValueError('Numero telephone est invalid')
        if v == "":
            raise ValueError('Numero telephone est required')
        return v.title()

    # address validation
    @validator('address')
    def addressValidator(cls, v):
        valid = re.compile('^([a-zA-Z0-9 ])+$')
        if valid.match(v) is None or len(v) < 3:
            raise ValueError('address est invalid')
        if v == "":
            raise ValueError('address est required')
        return v.title()

        # password validation
    @validator('password')
    def passwordValidator(cls, v):
        if v == "":
            raise ValueError('Mot de password est  required')
        if len(v) < 8:
            raise ValueError('Mot de password est trop courte')
        return v.title()

    @validator('email')
    def emailValidator(cls, v):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if v == "":
            raise ValueError('L\'address email est  required')
        if not re.fullmatch(regex, v):
            raise ValueError('L\'address email est invalid')
        return v.title()

    class UserLogin(BaseModel):
        email: str
        password: str

        @validator('password')
        def lpasswordValidator(cls, v):
            if v == "":
                raise ValueError('Mot de password est  required')
            return v.title()

        # validate email
        @validator('email')
        def logemailValidator(cls, v):
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if v == "":
                raise ValueError('L\'address email est  required')
            if not re.fullmatch(regex, v):
                raise ValueError('L\'address email est invalid')
            return v.title()

    class User_update(BaseModel):
        email: str
        password: Optional[str]
        full_name: str
