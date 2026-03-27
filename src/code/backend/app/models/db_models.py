from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Study(Base):
    __tablename__ = "studies"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    patient_name = Column(String(255))
    dicom_key = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    study_id = Column(Integer, nullable=False)
    status = Column(String(50), default="pending")
    result_key = Column(String(500))
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())