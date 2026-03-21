import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

def get_conn():
    return psycopg2.connect(
        user='postgres',
        password='root', 
        host='localhost',
        port='5432',
        database='tendance_db'
    )

# j'utilise "sqlite://" pour que SQLAlchemy ne cherche PAS le plugin postgresql
engine = create_engine("sqlite://", creator=get_conn)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
