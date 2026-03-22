


from sqlalchemy.orm import Session
from ..models import Indicateur
from ..schemas import IndicateurBase

#Retourne tous les indicateurs de la base de données.
def get_all(db: Session):
    return db.query(Indicateur).all()

# Retourne un indicateur précis par son id.
def get_by_id(db: Session, indicateur_id: int):
    return db.query(Indicateur).filter(Indicateur.id == indicateur_id).first()

# Retourne tous les indicateurs d'une catégorie précise.
def get_by_categorie(db: Session, category_id: int):
    return db.query(Indicateur).filter(Indicateur.category_id == category_id).all()


# Crée un nouvel indicateur en base de données.
def create(db: Session, data: IndicateurBase ):
    indicateur = Indicateur(name=data.name,
                           unit=data.unit,
                        description=data.description,
                           category_id=data.category_id)
    db.add(indicateur)
    db.commit()
    db.refresh(indicateur)
    return indicateur


