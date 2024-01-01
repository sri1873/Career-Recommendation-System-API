from datetime import date
from typing import List,Optional

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
    first_name: Optional[str]
    last_name: Optional[str]
    date_of_birth: Optional[date]
    phone_number: Optional[int]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    linkedin: Optional[str]
    profile_img: Optional[str]

    class Config:
        fields = {"date_of_birth": "dateOfBirth", "phone_number": "phoneNumber"}
