from datetime import datetime
import httpx
from sqlalchemy.orm import Session
from abc import ABC, abstractmethod
from models import Tendance, Historique, SourceAPI
from database import SessionLocal


class BaseCollecteur(ABC):
    """
    Classe mère abstraite pour tous les collecteurs de données.
    Contient la logique commune à toutes les APIs.
    Chaque classe fille doit implémenter la méthode transformer().
    """

    def __init__(self, source_id: int):
        """
        Initialise le collecteur.

        Paramètres :
            source_id : l'id de la source API dans la table sources_api
                        exemple : 1 pour World Bank, 4 pour Frankfurter...
        """
        # Identifiant de la source API dans la base de données
        self.source_id = source_id

        # Ouverture d'une session PostgreSQL
        self.session: Session = SessionLocal()

    async def collecter(self):
        """
        Méthode principale — orchestre tout le processus de collecte.
        Elle appelle les 3 étapes dans l'ordre :
            1. appeler_api()  → récupère les données brutes
            2. transformer()  → adapte les données au format de la base
            3. sauvegarder()  → compare et sauvegarde en base
        """
        # Étape 1 : appel de l'API
        reponse = await self.appeler_api()

        # Si l'API est inaccessible ou renvoie une erreur → on arrête
        if reponse is None:
            return

        # Étape 2 : transformation des données brutes
        donnees = self.transformer(reponse)

        # Étape 3 : sauvegarde en base
        await self.sauvegarder(donnees)


    """
        Fait la requête HTTP vers l'API externe.
        Récupère l'URL depuis la table sources_api grâce à self.source_id.

        Retourne :
            Le JSON de la réponse si succès
            None si erreur
        """
    async def appeler_api(self):

        # Récupère la source API depuis la base de données
        source = self.session.query(SourceAPI).filter(SourceAPI.id == self.source_id).first()
        try:
            # Appel HTTP asynchrone avec un timeout de 10 secondes
            async with httpx.AsyncClient() as client:
                reponse = await client.get(source.url_base, timeout=10)
                reponse.raise_for_status()

                # Retourne la réponse en JSON
                return reponse.json()

        except Exception as e:
            # Affiche l'erreur sans faire planter le programme
            print(f"Erreur appel API {source.nom} : {e}")
            return None


    """
        Méthode abstraite — DOIT être redéfinie dans chaque classe fille.
        Transforme la réponse brute de l'API en une liste de dictionnaires
        prêts à être sauvegardés en base.

        Paramètres :
            reponse : le JSON brut retourné par appeler_api()

        """

    @abstractmethod
    def transformer(self, reponse):
        pass


    """
       Compare et sauvegarde les données en base.

       Logique :
           - Si la tendance n'existe pas → INSERT tendances + INSERT historiques
           - Si la valeur est identique   → ne rien faire
           - Si la valeur est différente  → UPDATE tendances + INSERT historiques

       Paramètres :
           donnees : liste de dictionnaires retournée par transformer()
       """
    async def sauvegarder(self, donnees: list):

        for donnee in donnees:

            # Cherche si une tendance existe déjà
            # pour cet indicateur et ce pays
            tendance_existante = self.session.query(Tendance).filter(
                Tendance.indicateur_id == donnee["indicateur_id"],
                Tendance.pays == donnee["pays"]
            ).first()

            if tendance_existante:
                # La tendance existe — on compare les valeurs
                if tendance_existante.valeur == donnee["valeur"]:
                    # Même valeur → pas de changement, on passe au suivant
                    continue
                if donnee["date_heure"] > tendance_existante.date_heure:
                # Valeur différente → on met à jour la tendance actuelle
                    tendance_existante.valeur     = donnee["valeur"]
                    tendance_existante.date_heure = donnee["date_heure"]

            else:
                # La tendance n'existe pas encore → on la crée
                nouvelle_tendance = Tendance(
                    valeur        = donnee["valeur"],
                    pays          = donnee["pays"],
                    indicateur_id = donnee["indicateur_id"],
                    source_id     = self.source_id,
                    date_heure    = donnee["date_heure"]
                )
                self.session.add(nouvelle_tendance)

            # Dans tous les cas (nouvelle tendance ou valeur différente)
            # on archive la valeur dans l'historique
            nouvel_historique = Historique(
                valeur        = donnee["valeur"],
                pays          = donnee["pays"],
                indicateur_id = donnee["indicateur_id"],
                date_heure    = donnee["date_heure"]
            )
            self.session.add(nouvel_historique)

            # Sauvegarde en base de données
            self.session.commit()