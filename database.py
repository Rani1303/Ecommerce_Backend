from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid
from sqlalchemy.dialects.postgresql import UUID

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

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()