from fastapi import FastAPI, Depends
from typing import List
from sqlalchemy.orm import Session
import src.schemas.garment_schema as garment_schema
from src.repositories.database import SessionLocal, engine
from src.repositories import garment_repository
from src.repositories.garment_model import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/garments",
         tags=["garments"],
         summary="Get all garments",
         response_model=List[garment_schema.Garment])
def get_garments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return garment_repository.get_garments(db, skip=skip, limit=limit)


@app.get("/garments/{garment_id}",
         tags=["garments"],
         summary="Get garment by id",
         response_model=garment_schema.Garment)
def get_garment(garment_id: int, db: Session = Depends(get_db)):
    garment = garment_repository.get_garment(db, garment_id=garment_id)
    return garment


@app.post("/garments",
          tags=["garments"],
          summary="Create garment",
          status_code=201,
          response_model=garment_schema.Garment)
def create_garment(garment: garment_schema.GarmentCreate, db: Session = Depends(get_db)):
    db_garment = garment_repository.create_garment(db, garment)
    return db_garment


@app.put("/garments/{garment_id}",
         tags=["garments"],
         summary="Update garment by id",
         )
def update_garment(garment_id: int, garment: garment_schema.GarmentCreate, db: Session = Depends(get_db)):
    return garment_repository.update_garment(db, garment_id=garment_id, garment=garment)


@app.delete("/garments/{garment_id}",
            tags=["garments"],
            summary="Delete garment by id",
            status_code=204)
def delete_garment(garment_id: int, db: Session = Depends(get_db)):
    garment_repository.delete_garment(db, garment_id=garment_id)

