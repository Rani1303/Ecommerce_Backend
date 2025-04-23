from sqlalchemy import create_engine, Column, Integer, String, Float, Text, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

SQLALCHEMY_DATABASE_URL="postgresql://postgres:postgres@localhost:5432/ecommerce"

engine=create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base=declarative_base()

class Product(Base):
    __tablename__="products"
    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name=Column(String(100), nullable=False)
    description=Column(Text)
    price=Column(Float, nullable=False)
    stock=Column(Integer, default=0)

class User(Base):
    __tablename__= "users"
    id= Column(UUID(as_uuid= True), primary_key=True, default=uuid.uuid4)
    username=Column(String(50), unique=True,nullable=False)
    email=Column(String(100), unique= True, nullable=False)
    password=Column(String(100), nullable=False)
    is_active=Column(Boolean, default=True)
    created_at=Column(DateTime, default=datetime.utcnow)
    updated_at=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()