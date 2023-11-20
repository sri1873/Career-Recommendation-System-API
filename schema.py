from datetime import date
from typing import List

from pydantic import BaseModel, EmailStr


class EmailBody(BaseModel):
    to: str
    subject: str
    message: str


class Login(BaseModel):
    email_id: str
    password: str

    class Config:
        fields = {"email_id": "emailId", "password": "password"}


class CreateUser(BaseModel):
    role: str
    email_id: str
    password: str
    first_name: str
    last_name: str
    date_of_birth: date
    phone_number: int

    class Config:
        fields = {
            "email_id": "emailId",
            "date_of_birth": "dateOfBirth",
            "phone_number": "phoneNumber",
        }


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
        fields = {"date_of_birth": "dateOfBirth", "phone_number": "phoneNumber"}
