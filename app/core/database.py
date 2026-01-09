from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg://postgres:PASSWORD@localhost:5432/wa_roadhelp"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

def get_db():
    """
    Dependency that provides a db session and closes it after request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()