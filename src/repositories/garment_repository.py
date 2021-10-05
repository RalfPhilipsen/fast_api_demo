from sqlalchemy.orm import Session
from src.schemas.garment_schema import GarmentCreate
from src.repositories.garment_model import Garment
from fastapi import HTTPException
from typing import List


def create_garment(db: Session, garment: GarmentCreate) -> Garment:
    db_garment = Garment(
        brand_name=garment.brand_name,
        type=garment.type,
        price=garment.price,
        color=garment.color
    )
    db.add(db_garment)
    db.commit()
    db.refresh(db_garment)
    return db_garment


def get_garment(db: Session, garment_id: int) -> Garment:
    garment = db.query(Garment).filter(Garment.id == garment_id).first()
    if garment is None:
        raise HTTPException(status_code=404, detail='Garment not found')
    return garment


def get_garments(db: Session, skip: int = 0, limit: int = 100) -> List[Garment]:
    return db.query(Garment).offset(skip).limit(limit).all()


def delete_garment(db: Session, garment_id: int) -> None:
    deleted = db.query(Garment).filter(Garment.id == garment_id).delete()
    if deleted == 0:
        raise HTTPException(status_code=404, detail='Garment not found')
    db.commit()


def update_garment(db: Session, garment_id: int, garment: GarmentCreate) -> Garment:
    updated = db.query(Garment).filter(Garment.id == garment_id).update({
        Garment.type: garment.type,
        Garment.brand_name: garment.brand_name,
        Garment.price: garment.price,
        Garment.color: garment.color
    })
    if updated == 0:
        raise HTTPException(status_code=404, detail='Garment not found')
    db.commit()

    updated_garment = get_garment(db, garment_id=garment_id)
    return updated_garment
