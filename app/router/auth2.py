from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import JWTError

from app.database import get_db
from app.auth2 import service, tokens, schemas

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=schemas.TokenResponse)
def login(data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = service.authenticate_user(db, data.username, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token, refresh_token = service.generate_tokens(user)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh", response_model=schemas.TokenResponse)
def refresh_token(data: schemas.RefreshRequest):
    try:
        payload = tokens.decode_token(data.refresh_token, refresh=True)
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        user_data = {"sub": username}
        access_token = tokens.create_access_token(user_data)
        refresh_token = tokens.create_refresh_token(user_data)
        return {"access_token": access_token, "refresh_token": refresh_token}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")


@router.post("/register", response_model=schemas.UserResponse)
def register(data: schemas.UserRegisterRequest, db: Session = Depends(get_db)):
    user = service.create_user(db, data.username, data.password)
    return {"username": user.username}


@router.post("/change-password", response_model=schemas.UserResponse)
def change_password(data: schemas.ChangePasswordRequest, db: Session = Depends(get_db)):
    user = service.change_password(
        db, data.username, data.old_password, data.new_password
    )
    return {"username": user.username}


@router.post("/delete", response_model=schemas.DeletionResponse)
def delete_user(data: schemas.DeleteUserRequest, db: Session = Depends(get_db)):
    return service.delete_user(db, data.username, data.password)
