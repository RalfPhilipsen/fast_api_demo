from fastapi import FastAPI, Depends, Request, Response
from typing import List
from sqlalchemy.orm import Session
import src.schemas.garment_schema as garment_schema
from src.repositories.database import SessionLocal, engine
from src.repositories import garment_repository
from src.repositories.garment_model import Base
from src.repositories.garment_model import Garment

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Garments Management",
    description="UI for managing garments",
    version="0.0.1"
)


@app.middleware(middleware_type="http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


def get_db(request: Request):
    return request.state.db


@app.get(path="/garments",
         tags=["garments"],
         summary="Get all garments",
         response_model=List[garment_schema.Garment])
def get_garments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> List[Garment]:
    return garment_repository.get_garments(db, skip=skip, limit=limit)


@app.get(path="/garments/{garment_id}",
         tags=["garments"],
         summary="Get garment by id",
         response_model=garment_schema.Garment)
def get_garment(garment_id: int, db: Session = Depends(get_db)) -> Garment:
    return garment_repository.get_garment(db, garment_id=garment_id)


@app.post(path="/garments",
          tags=["garments"],
          summary="Create garment",
          status_code=201,
          response_model=garment_schema.Garment)
def create_garment(garment: garment_schema.GarmentCreate, db: Session = Depends(get_db)) -> Garment:
    return garment_repository.create_garment(db, garment)


@app.put(path="/garments/{garment_id}",
         tags=["garments"],
         summary="Update garment by id",
         )
def update_garment(garment_id: int, garment: garment_schema.GarmentCreate, db: Session = Depends(get_db)) -> Garment:
    return garment_repository.update_garment(db, garment_id=garment_id, garment=garment)


@app.delete("/garments/{garment_id}",
            tags=["garments"],
            summary="Delete garment by id",
            status_code=204)
def delete_garment(garment_id: int, db: Session = Depends(get_db)) -> None:
    garment_repository.delete_garment(db, garment_id=garment_id)

