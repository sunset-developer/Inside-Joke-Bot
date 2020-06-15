import os
import traceback

from aiopg.sa import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DB_LOGIN
import asyncio
from gino import Gino

engine = create_engine(DB_LOGIN)
Base = declarative_base()
Base.metadata.create_all(engine)

def create_session():
    Session = sessionmaker(bind=engine, autocommit=True)
    session = Session()
    return session



