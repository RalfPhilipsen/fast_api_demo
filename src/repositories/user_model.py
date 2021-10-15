from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.repositories.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)

    garments = relationship("Garment", back_populates="owner")