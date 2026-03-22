from pydoc import describe

from database import SessionLocal
from models import Categorie, Indicateur, SourceAPI


def insert_categories(db):
    categories = [
        Categorie( name = "Économie"),
        Categorie(name = "Énergie"),
        Categorie(name = "Environnement"),
        Categorie(name = "Finance"),
        Categorie(name = "Bourse"),
        Categorie(name = "Social"),
    ]
    db.add_all(categories)
    db.commit()
    print("Catégories insérées")

def insert_indicateurs(db):
    indicateurs = [
        Indicateur(
            name = "PIB",
            unit = "USD",
            category_id = 1,
            description = "Produit Intérieur Brut courant"
        ),
    ]