from sqlalchemy.orm import Session
from models import Tendance
from schemas import TendanceBase
from datetime import datetime

# Retourne toutes les tendances de la base de données.
def get_all(db: Session):
    return db.query(Tendance).all()

#  Retourne une tendance précise par son id.
def get_by_id(db: Session, tendance_id: int):
    return db.query(Tendance).filter(Tendance.id == tendance_id).first()

# Retourne toutes les tendances d'un indicateur précis.
def get_by_indicateur(db: Session, indicateur_id: int):
    return db.query(Tendance).filter(Tendance.indicateur_id == indicateur_id).all()

# Retourne toutes les tendances d'un pays précis.
def get_by_pays(db: Session, pays: str):
    return db.query(Tendance).filter(Tendance.pays == pays).all()

# Crée une nouvelle tendance en base de données.
def create(db: Session, data: TendanceBase):
    tendance = Tendance(valeur = data.valeur,
                        pays = data.pays,
                        source_id = data.source_id,
                        indicateur_id = data.indicateur_id)
    db.add(tendance)
    db.commit()
    db.refresh(tendance)
    return tendance

#Met à jour la valeur actuelle d'une tendance existante.
def update(db: Session, pays:str, indicateur_id: int, data: TendanceBase):
    tendance = db.query(Tendance).filter(Tendance.pays == pays,
                              Tendance.indicateur_id == indicateur_id).first()

    if tendance:
        tendance.valeur = data.valeur
        tendance.date_heure = datetime.utcnow()
        db.commit()
        db.refresh(tendance)

    return tendance

