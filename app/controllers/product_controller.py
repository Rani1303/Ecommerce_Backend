from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..schemas.product import ProductCreate, ProductResponse
from ..repositories.product_repository import ProductRepository
from ..database import get_db
from ..dependencies.auth import get_current_user
from ..models.user import User

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product_repo = ProductRepository(db)
    return product_repo.get_all(skip, limit)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product_repo = ProductRepository(db)
    product = product_repo.get_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product_repo = ProductRepository(db)
    return product_repo.create(product.dict())

@router.delete("/{product_id}")
def delete_product(
    product_id: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product_repo = ProductRepository(db)
    if product_repo.delete(product_id):
        return {"message": "Product deleted successfully"}
    raise HTTPException(status_code=404, detail="Product not found") 