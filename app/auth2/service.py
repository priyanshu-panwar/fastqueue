from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.auth2.models import User
from app.auth2.tokens import create_access_token, create_refresh_token
from datetime import timedelta
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_EXPIRE_MINUTES = 15
REFRESH_EXPIRE_DAYS = 7


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not pwd_context.verify(password, user.password_hash):
        return None
    return user


def generate_tokens(user: User):
    user_data = {"sub": user.username}
    access_token = create_access_token(user_data)
    refresh_token = create_refresh_token(user_data)
    return access_token, refresh_token


def create_user(db: Session, username: str, password: str):
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User(username=username, password_hash=pwd_context.hash(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def change_password(db: Session, username: str, old_password: str, new_password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not pwd_context.verify(old_password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user.password_hash = pwd_context.hash(new_password)
    db.commit()
    return user


def delete_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not pwd_context.verify(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    db.delete(user)
    db.commit()
    return {"detail": f"User {username} deleted successfully"}
