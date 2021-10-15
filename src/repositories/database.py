from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import yaml
import os


with open(os.path.join("src", "config", "conf.yml"), 'r') as stream:
    config = yaml.safe_load(stream)
    SQLALCHEMY_DATABASE_URL = config['SQLALCHEMY_DATABASE_URL']

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
