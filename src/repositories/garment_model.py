from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from src.repositories.database import Base


class Garment(Base):
    __tablename__ = "garments"

    id = Column(Integer, primary_key=True, index=True)
    brand_name = Column(String)
    type = Column(String)
    price = Column(Float)
    color = Column(String)