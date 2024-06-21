# utils.py
from sqlalchemy.orm import Session
from models import User

def validate_username_unique(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if user:
        raise ValueError('Username already exists')

def validate_email_unique(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    if user:
        raise ValueError('Email address already registered')
