from sqlalchemy.orm import Session
from src.schemas.user_schema import UserCreate
from src.repositories.user_model import User
from fastapi import HTTPException


def create_user(db: Session, user: UserCreate) -> User:
    try:
        db_user = User(
            **user.dict()
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user
    except Exception as e:
        if "psycopg2.errors.UniqueViolation" in e.args[0]:
            raise HTTPException(status_code=409, detail='E-mail address is already in use')
        raise e


def get_user(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user
