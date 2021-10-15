from pydantic import BaseModel
from enum import Enum


class ProductType(str, Enum):
    trousers = "trousers"
    jacket = "jacket"
    shoes = "shoes"


class GarmentBase(BaseModel):
    brand_name: str
    type: ProductType
    price: float
    color: str


class GarmentCreate(GarmentBase):
    pass


class Garment(GarmentBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
