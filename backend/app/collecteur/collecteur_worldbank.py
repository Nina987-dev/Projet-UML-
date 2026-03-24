
from datetime import datetime
from .base_collecteur import BaseCollecteur
from models import SourceAPI
import httpx


class CollecteurWorldBank(BaseCollecteur):
    PAYS = "FR;DE;US;GB;IT;JP;CA;CN"

    INDICATEURS = {
        1: "NY.GDP.MKTP.CD",    # PIB
        2: "FP.CPI.TOTL.ZG",   # Inflation
        3: "SL.UEM.TOTL.ZS",   # Chômage
        4: "NY.GDP.PCAP.CD",   # PIB par habitant
        5: "GC.DOD.TOTL.GD.ZS", # Dette publique
        8: "EN.GHG.CO2.PC.CE.AR5", # Émissions CO2
    }
    async def appeler_api(self):
        source=  self.session.query(SourceAPI).filter(SourceAPI.id == self.source_id, SourceAPI.name == "World Bank").first()

        resultat = []
        for indicateur_id, code in self.INDICATEURS.items():
            url = f"{source.url_base}/{self.PAYS}/indicator/{code}?format=json&per_page=1000"

            try :
                async with httpx.AsyncClient() as client:
                    reponse = await client.get(url, timeout=30)
                    reponse.raise_for_status()
                    resultat.append((indicateur_id, reponse.json()))

                    print(f"{code} récupéré")

            except Exception as e:
                print(f" Erreur pour{code} : {e}")
        return resultat

    def transformer(self, reponse):
        donnees = []
        for indicateur_id, reponse_json in reponse:

        # Vérifie que la réponse a bien 2 éléments
            if not isinstance(reponse_json, list) or len(reponse_json) < 2:
                print(f"Réponse invalide pour indicateur {indicateur_id} : {reponse_json}")
                continue

            entries = reponse_json[1]

        # Vérifie que entries n'est pas None
            if entries is None:
                continue

            for entry in entries:
                if entry["value"] is None:
                    continue
                donnees.append({
                    "indicateur_id" : indicateur_id,
                    "pays"          : entry["country"]["value"],
                    "valeur"        : entry["value"],
                    "date_heure"    : datetime(int(entry["date"]), 1, 1)
                })
        return donnees

