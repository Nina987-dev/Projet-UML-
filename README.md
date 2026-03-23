# Projet-UML-

# Plateforme de Visualisation de Données en Temps Réel

## Description
Ce projet consiste en la conception et la réalisation d’une plateforme web permettant de visualiser des tendances mondiales en temps réel (économiques, sociales, politiques, etc.).

L’application récupère des données depuis des API externes, les traite, puis les restitue sous forme de graphiques interactifs afin de faciliter leur analyse et leur compréhension.

---

## Objectifs
- Fournir une visualisation claire et dynamique des tendances mondiales
- Permettre le filtrage des données par catégories
- Afficher des graphiques interactifs en temps réel
- Conserver un historique des données

---

## Stack technique

### Frontend
- React
- Vite
- Axios
- Recharts

### Backend
- Python
- FastAPI
- Pydantic
- SQLAlchemy
- httpx
- pandas

### Base de données
- PostgreSQL

### Outils
- GitHub
- Notion
- Postman
- Draw.io / Visual Paradigm
- Figma

---

## Fonctionnalités principales
- Intégration d’API externes pour la récupération des données
- Traitement et transformation des données
- Visualisation via des graphiques interactifs
- Filtrage par catégories (économie, politique, etc.)
- Consultation de l’historique des tendances

---

## Équipe
Groupe C

- Chef de projet : Celina CHEBALLAH
- Responsable backend : Adama BA
- Responsable UML/ analyse : Dalya GHALEB
- Responsable tests / documentation : Karima GAUTIH
- Responsable frontend : Nasifa Zabalmougamadou

---

## Lancement du projet

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

