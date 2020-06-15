from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import DB_LOGIN

engine = create_engine(DB_LOGIN)
Base = declarative_base()
Base.metadata.create_all(engine)


def create_session():
    Session = sessionmaker(bind=engine, autocommit=True)
    session = Session()
    return session
