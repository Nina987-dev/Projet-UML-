import csv
import io
from .base_collecteur import BaseCollecteur
from models import SourceAPI, Indicateur
import httpx
from datetime import datetime


class CollecteurFRED(BaseCollecteur):
    """
    Collecteur pour l'API FRED (Federal Reserve Economic Data).
    Récupère les taux directeurs de la Fed et de la BCE.
    Les données sont retournées en CSV — on prend uniquement
    la dernière ligne (valeur la plus récente).
    """

    # { nom en base : (code FRED, pays) }
    INDICATEURS = {
        "Taux Fed" : ("FEDFUNDS", "Etats-Unis"),
        "Taux BCE" : ("ECBDFR",   "Europe"),
    }

    async def appeler_api(self):
        """
        Appelle FRED pour chaque indicateur.
        Retourne une liste de tuples (indicateur_id, pays, contenu_csv)
        """
        source = self.session.query(SourceAPI) \
            .filter(SourceAPI.id == self.source_id) \
            .first()

        donnees = []

        for nom, (code, pays) in self.INDICATEURS.items():

            # Récupère l'id de l'indicateur en base
            indicateur = self.session.query(Indicateur) \
                .filter(Indicateur.name == nom) \
                .first()

            # Construit l'URL
            url = f"{source.url_base}?id={code}"

            try:
                async with httpx.AsyncClient() as client:
                    reponse = await client.get(url, timeout=10)
                    reponse.raise_for_status()
                    donnees.append((indicateur.id, pays, reponse.text))
                    print(f"{nom} récupéré")
            except Exception as e:
                print(f"Erreur pour {nom} : {e}")

        return donnees

    def transformer(self, reponse):
        """
        Transforme le CSV de FRED en liste de dictionnaires.
        On prend uniquement la dernière ligne de chaque CSV
        car elle contient la valeur la plus récente.
        """
        donnees = []

        for indicateur_id, pays, contenu_csv in reponse:

            # Parse le CSV
            reader  = csv.reader(io.StringIO(contenu_csv))
            next(reader)        # saute l'en-tête (DATE, valeur)
            lignes  = list(reader)

            if not lignes:
                print(f"CSV vide pour indicateur {indicateur_id}")
                continue

            # Prend uniquement la dernière ligne
            derniere = lignes[-1]
            date_str = derniere[0]   # ex: "2026-02-01"
            valeur   = derniere[1]   # ex: "5.25"

            # Ignore les valeurs vides
            if not valeur:
                print(f"Valeur vide pour indicateur {indicateur_id}")
                continue

            donnees.append({
                "indicateur_id" : indicateur_id,
                "pays"          : pays,
                "valeur"        : float(valeur),
                "date_heure"    : datetime.strptime(date_str, "%Y-%m-%d")
            })

        return donnees