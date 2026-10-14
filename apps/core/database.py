from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


from apps.core.config import settings

engine = create_engine(url=settings.database_url)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        None