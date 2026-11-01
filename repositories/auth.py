from models.auth import Users
from sqlalchemy.orm import Session
from servise.dto import UserRegisterDTO

def user_register(db: Session, data: UserRegisterDTO):
    user = Users(email=data.email,  hashed_password=data.hash_password, full_name=data.full_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def user_get_email(db: Session, email: str):
    return db.query(Users).filter(Users.email == email).first()
    