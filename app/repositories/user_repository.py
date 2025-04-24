from sqlalchemy.orm import Session
from ..models.user import User
import bcrypt

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> User:
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def create(self, user_data: dict) -> User:
        hashed_password = bcrypt.hashpw(user_data["password"].encode(), bcrypt.gensalt()).decode()
        user_data["password"] = hashed_password
        db_user = User(**user_data)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode()) 