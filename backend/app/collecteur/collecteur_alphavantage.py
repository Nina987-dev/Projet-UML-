from .base_collecteur import BaseCollecteur
from models import SourceAPI, Indicateur
import httpx
import os
from dotenv import load_dotenv
from datetime import datetime
class CollecteurAlphavantage(BaseCollecteur):
    load_dotenv()
    API_KEY = os.getenv("ALPHAAVANTAGE")

    ACTIONS = {
        "Apple" : "AAPL",
        "Google" : "GOOGL",
        "Microsoft" : "MSFT",
        "TotalEnergies": "TTE"
    }
    CRYPTOS = {
        "Bitcoin" : "BTC",
    }
    async def appeler_api(self):

        source = self.session.query(SourceAPI) \
        .filter(SourceAPI.id == self.source_id) \
        .first()

        donnees = []

        # Boucle 1 — actions (une requête par action)
        for nom, symbole in self.ACTIONS.items():
            indicateur = self.session.query(Indicateur) \
            .filter(Indicateur.name == nom) \
            .first()

            url = f"{source.url_base}?function=GLOBAL_QUOTE&symbol={symbole}&apikey={self.API_KEY}"
            try:
                async with httpx.AsyncClient() as client:
                    reponse = await client.get(url, timeout=10)
                    reponse.raise_for_status()
                    donnees.append((indicateur.id, reponse.json()))
                    print(f"{nom} récupéré")
            except Exception as e:
                print(f"Erreur {nom} : {e}")

        # Boucle 2 — cryptos
        for nom, symbole in self.CRYPTOS.items():
            indicateur = self.session.query(Indicateur) \
            .filter(Indicateur.name == nom) \
            .first()

            url = f"{source.url_base}?function=CURRENCY_EXCHANGE_RATE&from_currency={symbole}&to_currency=USD&apikey={self.API_KEY}"
            try:
                async with httpx.AsyncClient() as client:
                    reponse = await client.get(url, timeout=10)
                    reponse.raise_for_status()
                    donnees.append((indicateur.id, reponse.json()))
                    print(f"{nom} récupéré")
            except Exception as e:
                print(f"Erreur {nom} : {e}")

        return
    def transformer(self, reponse):
        """
        Transforme la réponse d'Alpha Vantage en liste de dictionnaires.
        Gère deux formats différents :
        - GLOBAL_QUOTE pour les actions
        - CURRENCY_EXCHANGE_RATE pour les cryptos
        """
        donnees = []

        for indicateur_id, data in reponse:

        # Cas 1 — Action (GLOBAL_QUOTE)
            if "Global Quote" in data:
                quote = data["Global Quote"]

            # Si la réponse est vide → on passe
                if not quote:
                    print(f"Réponse vide pour indicateur {indicateur_id}")
                    continue

                valeur = float(quote["05. price"])
                date   = datetime.strptime(
                quote["07. latest trading day"],
                "%Y-%m-%d"
                )

            # Cas 2 — Crypto (CURRENCY_EXCHANGE_RATE)
            elif "Realtime Currency Exchange Rate" in data:
                rate = data["Realtime Currency Exchange Rate"]

                valeur = float(rate["5. Exchange Rate"])
                date   = datetime.strptime(
                rate["6. Last Refreshed"],
                "%Y-%m-%d %H:%M:%S"
                )

            else:
                print(f" Format inconnu pour indicateur {indicateur_id}")
                continue

            donnees.append({
            "indicateur_id" : indicateur_id,
            "pays"          : "Mondial",
            "valeur"        : valeur,
            "date_heure"    : date
            })

        return donnees



