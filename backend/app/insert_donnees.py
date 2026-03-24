

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
        # Catégorie Économie (category_id = 1)
        Indicateur(
            name        = "PIB",
            unit        = "USD",
            category_id = 1,
            description = "Produit Intérieur Brut en dollars courants"
        ),
        Indicateur(
            name        = "Inflation",
            unit        = "%",
            category_id = 1,
            description = "Variation annuelle des prix à la consommation"
        ),
        Indicateur(
            name        = "Chômage",
            unit        = "%",
            category_id = 1,
            description = "Pourcentage de la population active sans emploi"
        ),
        Indicateur(
            name        = "PIB par habitant",
            unit        = "USD",
            category_id = 1,
            description = "PIB divisé par la population totale du pays"
        ),
        Indicateur(
            name        = "Dette publique",
            unit        = "% PIB",
            category_id = 1,
            description = "Dette du gouvernement exprimée en % du PIB"
        ),
        # Catégorie Énergie (category_id = 2)
        Indicateur(
            name        = "Prix pétrole WTI",
            unit        = "USD/baril",
            category_id = 2,
            description = "Prix du baril de pétrole West Texas Intermediate"
        ),
        Indicateur(
            name        = "Prix pétrole Brent",
            unit        = "USD/baril",
            category_id = 2,
            description = "Prix du baril de pétrole Brent, référence mondiale"
        ),
        # Catégorie Environnement (category_id = 3)
        Indicateur(
            name        = "Émissions CO2",
            unit        = "tonnes/hab",
            category_id = 3,
            description = "Émissions de CO2 par habitant"
        ),
        # Catégorie Bourse (category_id = 5)
        Indicateur(
            name        = "Apple",
            unit        = "USD",
            category_id = 5,
            description = "Cours de l'action Apple Inc. (AAPL)"
        ),
        Indicateur(
            name        = "Google",
            unit        = "USD",
            category_id = 5,
            description = "Cours de l'action Alphabet Inc. (GOOGL)"
        ),
        Indicateur(
            name        = "Bitcoin",
            unit        = "USD",
            category_id = 5,
            description = "Prix du Bitcoin en dollars américains"
        ),
    ]
    db.add_all(indicateurs)
    db.commit()
    print("✅ Indicateurs insérés")

def insert_sources_api(db):
    sources = [
        SourceAPI(
            name        = "World Bank",
            url_base    = "https://api.worldbank.org/v2/country",
            category_id = 1  # Économie
        ),
        SourceAPI(
            name         = "World Bank",
            url_base    = "https://api.worldbank.org/v2/country",
            category_id = 2  # Énergie
        ),
        SourceAPI(
            name        = "World Bank",
            url_base    = "https://api.worldbank.org/v2/country",
            category_id = 3  # Environnement
        ),
    ]
    db.add_all(sources)
    db.commit()
    print("✅ Sources API insérées")

if __name__ == "__main__":

    db = SessionLocal()
    try:
        insert_categories(db)
        insert_indicateurs(db)
        insert_sources_api(db)
        print("les tables Catégories, SourceAPI et Indicateur sont remplies ! ")
    finally:
        db.close()