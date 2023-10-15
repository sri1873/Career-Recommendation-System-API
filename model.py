from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, DateTime, BigInteger, Time
from sqlalchemy.orm import relationship
from datetime import datetime, date
from sqlalchemy.ext.declarative import declarative_base


import uuid

Base = declarative_base()

class UserModel(Base):
    __tablename__ = 'user'
    _id = Column(String, primary_key=True,
                unique=True, default=uuid.uuid4)
    role = Column(String, default='STUDENT', nullable=False)
    email_id = Column(String, unique=True, nullable=False)
    password = Column(String, unique=True, nullable=False)
    phone_number = Column(BigInteger, unique=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    created_on = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String, nullable=True)
    updated_on = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    updated_by = Column(String, nullable=True)


