from datetime import date
from pydantic import BaseModel, EmailStr
from typing import List

class EmailSchema(BaseModel):
    email: List[EmailStr]
class Login(BaseModel):
    email_id: str
    password: str

    class Config:
        form_attributes = True


class CreateUser(BaseModel):
    role: str
    email_id: str
    password: str
    first_name: str
    last_name: str
    date_of_birth: date
    phone_number: int

    class Config:
        form_attributes = True


class UserDetails(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    phone_number: int
    address: str
    city: str
    state: str
    country: str

    class Config:
        form_attributes = True
