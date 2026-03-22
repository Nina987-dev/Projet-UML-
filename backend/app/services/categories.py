from sqlalchemy.orm import Session
from models import Categorie
from schemas import CategorieBase

# Retourne toutes les catégories de la base de données.
def get_all(db: Session):
    return db.query(Categorie).all()

# Retourne une catégorie précise ar son id.
def get_category(db: Session, category_id: int):
    return db.query(Categorie).filter(Categorie.id == category_id).first()

# Crée une nouvelle catégorie en base de données.
def create(db: Session, data: CategorieBase):
    categorie= Categorie(name=data.name)
    db.add(categorie)
    db.commit()
    db.refresh(categorie)
    return categorie