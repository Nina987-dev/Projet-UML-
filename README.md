# Projet-UML - Plateforme de Visualisation de Données en Temps Réel

** Description :
  Ce projet consiste en la conception et la réalisation d’une plateforme web permettant de visualiser des tendances mondiales en temps réel (économiques, sociales, politiques, etc.).
  L’application récupère des données depuis des API externes, les traite, puis les restitue sous forme de graphiques interactifs afin de faciliter leur analyse et leur compréhension par les utilisateurs. 

** Objectifs :
  Fournir une visualisation claire et dynamique des tendances mondiales. 
  Permettre le filtrage des données par catégories (Economie, Social, etc.). 
  Afficher des graphiques interactifs en temps réel pour le suivi des indicateurs. 
  Conserver un historique structuré des données pour l'analyse temporelle. 

** Stack Technique :
  * Frontend :
  Framework: React (via Vite) 
  Communication: Axios 
  Visualisation: Recharts 
  * Backend :
  Langage: Python 3.10+ 
  Framework: FastAPI 
  Validation: Pydantic 
  Base de données: PostgreSQL 
  ORM/SQL: SQLAlchemy et Psycopg2 
  * Outils de Collaboration
  Gestion de version: GitHub 
  Planification: Notion 
  Design/UML: Figma, Draw.io, Visual Paradigm


** Equipe (Groupe C) :
  Celina CHEBALLAH 
  Adama BA 
  Dalya GHALEB 
  Nasifa ZABALMOUGAMADOU
  Karima GAUTIH 

** Structure du Backend :
  * main.py: Point d'entrée de l'API FastAPI et définition des routes.
  * collecteur.py: Logique d'extraction et de sauvegarde des données (NewsAPI, AlphaVantage).
  * queries.py: Centralisation des requêtes SQL pour la base de données.
  * schemas.py: Modèles Pydantic pour la validation et le typage des données.
  * init_db.py: Script de création et réinitialisation des 7 tables PostgreSQL.
  * models.py: Définition des entités ORM SQLAlchemy.
  * database.py: Gestion de la connexion et de la session vers la base de données.
  
** Guide de lancement :
  1. Installation des dependances :
    Avant de lancer le projet, installez les bibliothèques nécessaires via le terminal :
    pip install fastapi uvicorn psycopg2-binary httpx python-dotenv sqlalchemy
  2. Configuration de la base de donnees :
    Assurez-vous que PostgreSQL est lancé et que vos identifiants sont renseignés dans le fichier .env. Initialisez ensuite la structure des tables :
    python init_db.py (Cette commande supprime les tables existantes et les recrée à neuf)
  3. Collecte des donnees :
    Exécutez le collecteur pour interroger les API externes et remplir la base de données :
    python collecteur.py
  4. Lancement du serveur API :
    Le serveur API fait le pont entre la base de données PostgreSQL et l'interface utilisateur. Pour démarrer le service, exécutez la commande suivante dans le dossier backend/app :
    python -m uvicorn main:app --reload
    Accès et Test de l'API
    Une fois le serveur actif, l'interface de programmation (API) devient accessible localement sur votre machine.
    * Points d'accès principaux (Endpoints) :
      Visualisation des tendances : http://127.0.0.1:8000/tendances
      Cette route exécute une requête SQL via queries.py pour extraire les dernières actualités et données financières stockées.
      Elle renvoie un flux de données structuré que le Frontend (React) consommera pour générer l'affichage.
      Historique par catégorie : http://127.0.0.1:8000/historique/{nom_categorie}
      Permet de récupérer l'évolution temporelle des indicateurs chiffrés.
  # Note technique : Si la page est vide (comme pour /historique/finance), cela signifie qu'aucune donnée numérique n'a été enregistrée pour cette catégorie exacte dans la base de données. Assurez-vous      d'utiliser le nom exact défini lors de l'initialisation (ex: Économie).
  * Documentation Interactive (Swagger UI) :
    FastAPI génère automatiquement une documentation interactive conforme aux normes OpenAPI, permettant de tester chaque route et de visualiser les schémas de données :
    URL de documentation : http://127.0.0.1:8000/docs.
  * Comprendre l'infrastructure technique :
    127.0.0.1 (Localhost) : Il s'agit de l'adresse de bouclage réseau de votre propre ordinateur.
    Port 8000 : Canal de communication logiciel réservé par défaut au serveur de développement FastAPI pour éviter les conflits.
    JSON (JavaScript Object Notation) : Format standard d'échange de données, permettant au Backend (Python) de transmettre des objets structurés au Frontend (JavaScript).
