from datetime import date
from typing import List

from pydantic import BaseModel


class EmailSchema(BaseModel):
    email: List[str]


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
    first_name: str | None
    last_name: str | None
    # date_of_birth: date
    phone_number: int | None
    city: str | None
    state: str | None
    country: str | None
    linkedin: str | None
    profile_img: str | None

    class Config:
        fields = {"date_of_birth": "dateOfBirth", "phone_number": "phoneNumber"}
