from database import SessionLocal
from models import Categorie, Indicateur, SourceAPI


def insert_categories(db):
    categories = [
        Categorie(name="Économie"),
        Categorie(name="Énergie"),
        Categorie(name="Environnement"),
        Categorie(name="Finance"),
        Categorie(name="Bourse"),
        Categorie(name="Social"),
    ]
    db.add_all(categories)
    db.commit()
    print(" Catégories insérées")


def insert_indicateurs(db):
    indicateurs = [

        # ── Économie (category_id = 1) ──────────────────────────────
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
            description = "Dette du gouvernement exprimée en pourcentage du PIB"
        ),

        # ── Énergie (category_id = 2) ───────────────────────────────
        Indicateur(
            name        = "Prix pétrole WTI",
            unit        = "USD/baril",
            category_id = 2,
            description = "Prix du baril de pétrole brut West Texas Intermediate, référence américaine"
        ),
        Indicateur(
            name        = "Prix pétrole Brent",
            unit        = "USD/baril",
            category_id = 2,
            description = "Prix du baril de pétrole brut Brent, référence mondiale"
        ),
        Indicateur(
            name        = "Prix gaz naturel",
            unit        = "USD/MMBtu",
            category_id = 2,
            description = "Prix du gaz naturel sur le marché Henry Hub aux États-Unis"
        ),
        Indicateur(
            name        = "Prix diesel",
            unit        = "USD/gallon",
            category_id = 2,
            description = "Prix du diesel Ultra Low Sulfur sur le marché américain"
        ),
        Indicateur(
            name        = "Prix essence",
            unit        = "USD/gallon",
            category_id = 2,
            description = "Prix de l'essence RBOB sur le marché américain"
        ),

        # ── Environnement (category_id = 3) ─────────────────────────
        Indicateur(
            name        = "Émissions CO2",
            unit        = "tonnes/hab",
            category_id = 3,
            description = "Émissions de CO2 par habitant"
        ),
        Indicateur(
            name        = "Superficie forestière",
            unit        = "%",
            category_id = 3,
            description = "Pourcentage du territoire couvert de forêts"
        ),
        Indicateur(
            name        = "Eau douce",
            unit        = "%",
            category_id = 3,
            description = "Prélèvements d'eau douce en pourcentage des ressources disponibles"
        ),
        Indicateur(
            name        = "Accès eau potable",
            unit        = "%",
            category_id = 3,
            description = "Pourcentage de la population ayant accès à l'eau potable"
        ),
        Indicateur(
            name        = "Qualité de l'air",
            unit        = "µg/m³",
            category_id = 3,
            description = "Concentration de particules fines PM2.5 dans l'air"
        ),

        # ── Finance (category_id = 4) ────────────────────────────────
        Indicateur(
            name        = "Taux de change",
            unit        = "EUR",
            category_id = 4,
            description = "Taux de change des principales devises par rapport à l'Euro"
        ),
        Indicateur(
            name        = "Prix Or",
            unit        = "USD/once",
            category_id = 4,
            description = "Prix de l'once troy d'or en dollars américains"
        ),
        Indicateur(
            name        = "Prix Argent",
            unit        = "USD/once",
            category_id = 4,
            description = "Prix de l'once troy d'argent en dollars américains"
        ),
        Indicateur(
            name        = "Taux Fed",
            unit        = "%",
            category_id = 4,
            description = "Taux directeur de la Réserve Fédérale américaine"
        ),
        Indicateur(
            name        = "Taux BCE",
            unit        = "%",
            category_id = 4,
            description = "Taux directeur de la Banque Centrale Européenne"
        ),

        # ── Bourse (category_id = 5) ─────────────────────────────────
        Indicateur(
            name        = "Apple",
            unit        = "USD",
            category_id = 5,
            description = "Cours de l'action Apple Inc. (AAPL) en dollars"
        ),
        Indicateur(
            name        = "Google",
            unit        = "USD",
            category_id = 5,
            description = "Cours de l'action Alphabet Inc. (GOOGL) en dollars"
        ),
        Indicateur(
            name        = "Microsoft",
            unit        = "USD",
            category_id = 5,
            description = "Cours de l'action Microsoft Corp. (MSFT) en dollars"
        ),
        Indicateur(
            name        = "TotalEnergies",
            unit        = "EUR",
            category_id = 5,
            description = "Cours de l'action TotalEnergies SE (TTE) en euros"
        ),
        Indicateur(
            name        = "Bitcoin",
            unit        = "USD",
            category_id = 5,
            description = "Prix du Bitcoin en dollars américains (BTC/USD)"
        ),

        # ── Social (category_id = 6) ─────────────────────────────────
        Indicateur(
            name        = "Population",
            unit        = "habitants",
            category_id = 6,
            description = "Population totale du pays"
        ),
        Indicateur(
            name        = "Espérance de vie",
            unit        = "années",
            category_id = 6,
            description = "Espérance de vie à la naissance en années"
        ),
        Indicateur(
            name        = "Taux de pauvreté",
            unit        = "%",
            category_id = 6,
            description = "Pourcentage de la population vivant sous le seuil de pauvreté"
        ),
        Indicateur(
            name        = "Inégalités (Gini)",
            unit        = "indice",
            category_id = 6,
            description = "Indice de Gini mesurant les inégalités de revenus (0=égalité parfaite, 1=inégalité totale)"
        ),
        Indicateur(
            name        = "Mortalité infantile",
            unit        = "‰",
            category_id = 6,
            description = "Nombre de décès d'enfants de moins d'1 an pour 1000 naissances vivantes"
        ),
    ]
    db.add_all(indicateurs)
    db.commit()
    print("Indicateurs insérés")


def insert_sources_api(db):
    sources = [
        # World Bank → Économie, Environnement, Social
        SourceAPI(
            name        = "World Bank",
            url_base    = "https://api.worldbank.org/v2/country",
            category_id = 1
        ),
        SourceAPI(
            name        = "World Bank",
            url_base    = "https://api.worldbank.org/v2/country",
            category_id = 3
        ),
        SourceAPI(
            name        = "World Bank",
            url_base    = "https://api.worldbank.org/v2/country",
            category_id = 6
        ),
        # OilPriceAPI → Énergie + Finance (Or, Argent)
        SourceAPI(
            name        = "OilPriceAPI",
            url_base    = "https://api.oilpriceapi.com/v1/prices/latest",
            category_id = 2
        ),
        SourceAPI(
            name        = "OilPriceAPI",
            url_base    = "https://api.oilpriceapi.com/v1/prices/latest",
            category_id = 4
        ),
        # Frankfurter → Finance (taux de change)
        SourceAPI(
            name        = "Frankfurter",
            url_base    = "https://api.frankfurter.dev/v1/latest",
            category_id = 4
        ),
        # FRED → Finance (taux directeurs)
        SourceAPI(
            name        = "FRED",
            url_base    = "https://fred.stlouisfed.org/graph/fredgraph.csv",
            category_id = 4
        ),
        # Alpha Vantage → Bourse
        SourceAPI(
            name        = "Alpha Vantage",
            url_base    = "https://www.alphavantage.co/query",
            category_id = 5
        ),
    ]
    db.add_all(sources)
    db.commit()
    print(" Sources API insérées")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        insert_categories(db)
        insert_indicateurs(db)
        insert_sources_api(db)
        print("Base de données peuplée !")
    finally:
        db.close()