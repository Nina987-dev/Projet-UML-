from .base_collecteur import BaseCollecteur
from models import SourceAPI, Indicateur
import httpx
from datetime import datetime


class CollecteurFrankfurter(BaseCollecteur):
    """
    Collecteur pour l'API Frankfurter (Banque Centrale Européenne).
    Récupère les taux de change quotidiens par rapport à l'Euro.
    L'id de l'indicateur est récupéré dynamiquement depuis la base.
    """

    DEVISES = "USD,GBP,JPY,CNY,CAD"

    async def appeler_api(self):
        """
        Appelle Frankfurter pour récupérer les taux de change.
        Retourne le JSON de la réponse.
        """
        source = self.session.query(SourceAPI) \
            .filter(SourceAPI.id == self.source_id) \
            .first()

        url = f"{source.url_base}?base=EUR&symbols={self.DEVISES}"

        try:
            async with httpx.AsyncClient() as client:
                reponse = await client.get(url, timeout=10)
                reponse.raise_for_status()
                print(" Taux de change récupérés")
                return reponse.json()
        except Exception as e:
            print(f"Erreur Frankfurter : {e}")
            return None

    def transformer(self, reponse):
        """
        Transforme la réponse de Frankfurter en liste de dictionnaires.
        Utilise le champ 'pays' pour stocker le code de la devise.
        L'id de l'indicateur est récupéré dynamiquement depuis la base.
        """
        # Récupère l'id de "Taux de change" dynamiquement
        indicateur = self.session.query(Indicateur) \
            .filter(Indicateur.name == "Taux de change") \
            .first()

        if indicateur is None:
            print("Indicateur 'Taux de change' non trouvé en base !")
            return []

        donnees = []
        date  = reponse["date"]
        rates = reponse["rates"]

        for devise, valeur in rates.items():
            if valeur is None:
                continue
            donnees.append({
                "indicateur_id" : indicateur.id,
                "pays"          : devise,
                "valeur"        : valeur,
                "date_heure"    : datetime.strptime(date, "%Y-%m-%d")
            })

        return donnees