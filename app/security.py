from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db import get_db
from app.utils import decode_token
from repositories.auth import user_get_email

oauth2_sheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

def get_current_user(token: str = Depends(oauth2_sheme),
                     db: Session = Depends(get_db)):
    exception = HTTPException(status_code=401, 
                              detail="Could not validate credentials",
                              headers={"WWW-Authenticate": "Bearer"})
    payload: dict =  decode_token(token=token)
    if  payload is None:
        raise exception
    email :str = payload.get('email')
    if email is None:
        raise exception
    user = user_get_email(db=db, email=email)
    if user is None:
        raise exception
    return user