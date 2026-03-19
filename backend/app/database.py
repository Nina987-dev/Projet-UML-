
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Charge les variables du fichier .env
load_dotenv()

# Récupère l'URL de connexion depuis le.env
DATABASE_URL = os.getenv("DATABASE_URL")

# Moteur SQLAlchemy — c'est lui qui parle à PostgreSQL
engine = create_engine(DATABASE_URL)

# SessionLocal — chaque requête aura sa propre session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base — classe mère que toutes les classes de models.py héritent
Base = declarative_base()


# Fonction utilitaire — fournit une session à chaque endpoint
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()