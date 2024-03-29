from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'sqlite:///./restaurant.db'  # database location

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})  # database engine creation

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # session creation

Base = declarative_base()


def get_db():  # method for db connection
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()