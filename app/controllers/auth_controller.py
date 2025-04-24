from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..schemas.user import UserCreate, UserResponse
from ..schemas.auth import Token
from ..repositories.user_repository import UserRepository
from ..services.auth_service import AuthService
from ..database import get_db
from ..dependencies.auth import get_current_user
from ..models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=Token)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    if user_repo.get_by_username(user.username) or user_repo.get_by_email(user.email):
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    # Create user
    db_user = user_repo.create(user.dict())
    
    # Generate token
    auth_service = AuthService(user_repo)
    return auth_service.generate_token_for_user(user.username)

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    return auth_service.authenticate_user(form_data.username, form_data.password)

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/logout")
async def logout():
    return {"message": "Successfully logged out!"} 