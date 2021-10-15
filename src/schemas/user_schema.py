from pydantic import BaseModel
from typing import List
from src.schemas.garment_schema import Garment


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    garments: List[Garment]

    class Config:
        orm_mode = True
