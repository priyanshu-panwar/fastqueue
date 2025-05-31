from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth2.tokens import decode_token
from app.auth2.models import User
from app.auth2.exceptions import credentials_exception

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    try:
        payload = decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception()
    except JWTError:
        raise credentials_exception()

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception()
    return user
