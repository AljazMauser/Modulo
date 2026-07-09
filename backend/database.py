import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Po privzetem uporabljamo podatke iz docker-compose.yml
# Po privzetem uporabljamo SQLite, ker Docker in PostgreSQL nista na voljo na sistemu
# Za preklop nazaj na PostgreSQL samo spremenite URL nazaj na postgresql://...
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", "sqlite:///./erp.db"
)

# Za SQLite je potreben dodaten parameter
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
