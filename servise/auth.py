from sqlalchemy.orm import Session
from shemas.auth import UserRegister
from repositories.auth import user_get_email, user_register
from servise.dto import UserRegisterDTO
import bcrypt
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES 
from datetime import datetime, timedelta, timezone
import jwt
from  servise.exceptions import ConflictError, UnauthorizedError

def hash_password(password: str):
    password_bytes=password.encode('utf-8')
    salt=bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(password:str, hashed_password:str):
    password_bytes  = password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes,hashed_bytes)

def creat_token(data: dict):
    to_encode=data.copy()
    exprite = datetime.now(timezone.utc)+timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp':exprite})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def register(db: Session, user:UserRegister):
        email = user_get_email(db=db,
                               email=user.email)
        if email is not None:
            raise ConflictError("User already exists")
        hashed_password=hash_password(password=user.password)
        user_dto=UserRegisterDTO(email=user.email,
                                 hash_password=hashed_password,
                                 full_name=user.full_name)
        result = user_register(db=db,
                               data= user_dto) 
        return{'status':'user created',
               'email':result.email,
               'full_name':result.full_name}

def login(db:Session, email: str, password: str):
        db_user = user_get_email(db=db,
                            email=email)
        if db_user is None:
            raise UnauthorizedError('Invalid email or password')
        if not verify_password(password, db_user.hashed_password):
            raise UnauthorizedError('Invalid email or password')
        token = creat_token(data={'email':email})
        return {
            "access_token": token, 
            "token_type": "bearer"
        }


