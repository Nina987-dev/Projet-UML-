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

    # { nom en base : code World Bank }
    INDICATEURS = {
        # Économie
        "PIB"                    : "NY.GDP.MKTP.CD",
        "Inflation"              : "FP.CPI.TOTL.ZG",
        "Chômage"                : "SL.UEM.TOTL.ZS",
        "PIB par habitant"       : "NY.GDP.PCAP.CD",
        "Dette publique"         : "GC.DOD.TOTL.GD.ZS",
        # Environnement
        "Émissions CO2"          : "EN.GHG.CO2.PC.CE.AR5",
        "Superficie forestière"  : "AG.LND.FRST.ZS",
        "Eau douce"              : "ER.H2O.FWTL.ZS",
        "Accès eau potable"      : "SH.H2O.SAFE.ZS",
        "Qualité de l'air"       : "EN.ATM.PM25.MC.M3",
        # Social
        "Population"             : "SP.POP.TOTL",
        "Espérance de vie"       : "SP.DYN.LE00.IN",
        "Taux de pauvreté"       : "SI.POV.DDAY",
        "Inégalités (Gini)"      : "SI.POV.GINI",
        "Taux d'alphabétisation" : "SE.ADT.LITR.ZS",
    }

    async def appeler_api(self):
        """
        Appelle World Bank pour chaque indicateur.
        Récupère l'id de chaque indicateur dynamiquement depuis la base.
        Retourne une liste de tuples (indicateur_id, reponse_json)
        """
        # Récupère l'URL de base depuis sources_api
        source = self.session.query(SourceAPI) \
            .filter(SourceAPI.id == self.source_id) \
            .first()

        resultats = []

        for nom, code in self.INDICATEURS.items():

            # Cherche l'id de l'indicateur par son nom en base
            indicateur = self.session.query(Indicateur) \
                .filter(Indicateur.name == nom) \
                .first()

            if indicateur is None:
                print(f"Indicateur '{nom}' non trouvé en base — on passe !")
                continue

            # Construit l'URL complète
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