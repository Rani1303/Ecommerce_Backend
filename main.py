from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from typing import Optional
from database import engine, get_db, Product, Base
from pydantic import BaseModel
import uuid

class ProductBase(BaseModel):
    name: str
    description: Optional[str]=None
    price: float
    stock: int

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: uuid.UUID

    class Config:
        from_attributes=True


# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
app=FastAPI(title="Ecommerce API")

@app.get("/products/", response_model=List[ProductResponse])
def get_products(skip: int=0, limit: int=100, db: Session=Depends(get_db)):
    products=db.query(Product).offset(skip).limit(limit).all()
    return products

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id : uuid.UUID, db:Session=Depends(get_db)):
    product=db.query(Product).filter(Product.id==product_id).first()
    if product is None:
        raise HTTPException(status_code=404, details="Product not found")
    return product

@app.post("/add_product/",response_model=ProductResponse)
def add_product(product: ProductCreate, db: Session=Depends(get_db)):
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return {"message":"Product successfully added!"}

@app.delete("/delete_product/{product_id}")
def delete_product(product_id: uuid.UUID, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    db.refresh(product)
    return {"message": "Product deleted successfully!"}

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


