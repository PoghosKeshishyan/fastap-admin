import os
from fastapi import Depends
from fastapi_login import LoginManager
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from .models import User
from .dependencies import get_db_session

load_dotenv() 

SECRET = os.getenv("SECRET_KEY")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
manager = LoginManager(SECRET, token_url="/users/login")

@manager.user_loader
def load_user(username: str, db: Session = Depends(get_db_session)):
    return db.query(User).filter(User.username == username).first()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)