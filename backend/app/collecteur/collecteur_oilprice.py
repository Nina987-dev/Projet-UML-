import os
from dotenv import load_dotenv
from .base_collecteur import BaseCollecteur
from models import SourceAPI, Indicateur
import httpx
from datetime import datetime

load_dotenv()

class CollecteurOilPrice(BaseCollecteur):

    API_KEY = os.getenv("OILPRICE_API_KEY")

    # Énergie (source_id = 4)
    INDICATEURS_ENERGIE = {
        "Prix pétrole WTI"   : "WTI_USD",
        "Prix pétrole Brent" : "BRENT_CRUDE_USD",
        "Prix gaz naturel"   : "NATURAL_GAS_USD",
        "Prix diesel"        : "DIESEL_USD",
        "Prix essence"       : "GASOLINE_USD",
    }

    # Finance (source_id = 5)
    INDICATEURS_FINANCE = {
        "Prix Or"     : "GOLD_USD",
        "Prix Argent" : "SILVER_USD",
    }

    INDICATEURS_PAR_SOURCE = {
        4 : INDICATEURS_ENERGIE,
        5 : INDICATEURS_FINANCE,
    }

    async def appeler_api(self):
        headers = {"Authorization": f"Token {self.API_KEY}"}

        source = self.session.query(SourceAPI)\
                     .filter(SourceAPI.id == self.source_id)\
                     .first()

        # Sélectionne uniquement les indicateurs de la catégorie
        indicateurs = self.INDICATEURS_PAR_SOURCE.get(self.source_id, {})

        donnees = []
        for nom, code in indicateurs.items():
            indicateur = self.session.query(Indicateur)\
                             .filter(Indicateur.name == nom)\
                             .first()

            url = f"{source.url_base}?by_code={code}"

            try:
                async with httpx.AsyncClient() as client:
                    reponse = await client.get(url, headers=headers, timeout=30)
                    reponse.raise_for_status()
                    donnees.append((indicateur.id, reponse.json()))
                    print(f" {nom} récupéré")
            except Exception as e:
                print(f"Erreur pour {nom} : {e}")

        return donnees

    def transformer(self, reponse):
        donnees = []
        for indicateur_id, data in reponse:
            valeur = data["data"]["price"]
            date   = datetime.fromisoformat(
                         data["data"]["created_at"].replace("Z", "+00:00")
                     )
            donnees.append({
                "indicateur_id" : indicateur_id,
                "pays"          : "Mondial",
                "valeur"        : valeur,
                "date_heure"    : date
            })
        return donnees