from sqlalchemy import create_engine, MetaData
from os import environ
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(environ.get("DB_URL_LOCAL"))
SessionLocal = sessionmaker(autoflush=False, bind=engine)
meta = MetaData()
# conn = engine.connect()
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.rollback()
    finally:
        db.close()
