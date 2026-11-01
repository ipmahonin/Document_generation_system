from fastapi import APIRouter, Depends, HTTPException
from shemas.auth import UserRegister
from db import get_db
from servise.auth import register, login
from sqlalchemy.orm import Session
from app.security import get_current_user
from models.auth import Users
from fastapi.security import OAuth2PasswordRequestForm
from  servise.exceptions import ConflictError, UnauthorizedError

auth = APIRouter()

@auth.post('/register', status_code=201)
def auth_register(data: UserRegister, db: Session = Depends(get_db)):
  try:
    return register(db=db,
                    user=data)
  except  ConflictError as e:
    raise HTTPException(status_code=409, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail="Server fail")

@auth.post('/login', status_code=200)
def auth_login(data: OAuth2PasswordRequestForm = Depends() , db: Session = Depends(get_db)):
  try:
    return login(db=db,
                 email= data.username,
                 password=data.password)
  except UnauthorizedError as e:
    raise HTTPException(status_code=401, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail='Server fail')

  
@auth.get('/me',status_code=200)
def auth_me(user: Users = Depends(get_current_user)):
  return{
    'email': user.email,
    'full_name': user.full_name,
    'created_at': user.created_at
  }
  