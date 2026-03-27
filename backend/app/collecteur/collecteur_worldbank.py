from .base_collecteur import BaseCollecteur
from models import SourceAPI, Indicateur
import httpx
from datetime import datetime


class CollecteurWorldBank(BaseCollecteur):
    """
    Collecteur pour l'API World Bank.
    Récupère les données économiques, environnementales et sociales
    pour 8 pays (France, Allemagne, USA, UK, Italie, Japon, Canada, Chine).
    Les ids des indicateurs sont récupérés dynamiquement depuis la base.
    """

    # Les 8 pays suivis (codes alpha-2 séparés par ;)

    PAYS = "FR;DE;US;GB;IT;JP;CA;CN"

    INDICATEURS_ECONOMIE = {
        "PIB"              : "NY.GDP.MKTP.CD",
        "Inflation"        : "FP.CPI.TOTL.ZG",
        "Chômage"          : "SL.UEM.TOTL.ZS",
        "PIB par habitant" : "NY.GDP.PCAP.CD",
        "Dette publique"   : "GC.DOD.TOTL.GD.ZS",
    }
    INDICATEURS_ENVIRONNEMENT = {
        "Émissions CO2"         : "EN.GHG.CO2.PC.CE.AR5",
        "Superficie forestière" : "AG.LND.FRST.ZS",
        "Eau douce"             : "ER.H2O.FWTL.ZS",
        "Accès eau potable"     : "SH.H2O.SMDW.ZS",
        "Qualité de l'air"      : "EN.ATM.PM25.MC.M3",
    }
    INDICATEURS_SOCIAL = {
        "Population"          : "SP.POP.TOTL",
        "Espérance de vie"    : "SP.DYN.LE00.IN",
        "Taux de pauvreté"    : "SI.POV.DDAY",
        "Inégalités (Gini)"   : "SI.POV.GINI",
        "Mortalité infantile" : "SP.DYN.IMRT.IN",
    }
    INDICATEURS_PAR_SOURCE = {
        1 : INDICATEURS_ECONOMIE,
        2 : INDICATEURS_ENVIRONNEMENT,
        3 : INDICATEURS_SOCIAL,
    }


    async def appeler_api(self):
        source = self.session.query(SourceAPI)\
                     .filter(SourceAPI.id == self.source_id)\
                     .first()

        # Sélectionne uniquement les indicateurs de la catégorie
        indicateurs = self.INDICATEURS_PAR_SOURCE.get(self.source_id, {})

        resultats = []
        for nom, code in indicateurs.items():
            indicateur = self.session.query(Indicateur)\
                             .filter(Indicateur.name == nom)\
                             .first()

            url = f"{source.url_base}/{self.PAYS}/indicator/{code}?format=json&per_page=1000"
            try:
                async with httpx.AsyncClient() as client:
                    reponse = await client.get(url, timeout=30)
                    reponse.raise_for_status()
                    resultats.append((indicateur.id, reponse.json()))
                    print(f"{nom} récupéré")
            except Exception as e:
                print(f" Erreur pour {nom} : {e}")

        return resultats

    def transformer(self, reponse):
        """
        Transforme la réponse brute de World Bank
        en liste de dictionnaires prêts à être sauvegardés.
        Ignore les entrées avec valeur None.
        """
        donnees = []

        for indicateur_id, reponse_json in reponse:

            # Vérifie que la réponse est valide
            if not isinstance(reponse_json, list) or len(reponse_json) < 2:
                print(f"Réponse invalide pour indicateur {indicateur_id}")
                continue

            entries = reponse_json[1]

            if entries is None:
                continue

            for entry in entries:
                # Ignore les valeurs nulles
                if entry["value"] is None:
                    continue

                donnees.append({
                    "indicateur_id" : indicateur_id,
                    "pays"          : entry["country"]["value"],
                    "valeur"        : entry["value"],
                    "date_heure"    : datetime(int(entry["date"]), 1, 1)
                })

        return donnees