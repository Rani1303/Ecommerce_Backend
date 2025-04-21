from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Float,Text


SQLALCHEMY_DATABASE_URL="postgresql://postgres:postgres@localhost:5432/ecommerce"

engine=create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base=declarative_base()

class Product(Base):
    __tablename__="products"
    id=Column(Integer, primary_key=True, index=True)
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