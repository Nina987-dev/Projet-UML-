

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text
from datetime import datetime

from sqlalchemy.orm import relationship

from database import Base


#categories, indicators, data_points, historique, sources_api, user, commentaire
class Categorie(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True,nullable=False)
    name = Column(String, unique=True, nullable=False)


    indicateurs = relationship("Indicateur", back_populates='categorie')
    sources = relationship("SourceAPI", back_populates='categorie')



class Indicateur(Base):
    __tablename__ = 'indicateurs'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    unit = Column(String(100))
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    description = Column(Text, nullable=True)
    categorie = relationship("Categorie", back_populates='indicateurs')

    tendances = relationship("Tendance", back_populates='indicateur')
    historique = relationship("Historique", back_populates='indicateur')

class SourceAPI(Base):
    __tablename__ = 'sources_api'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    url_base = Column(String(100), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)

    # une source appartient à une catégorie.
    categorie = relationship("Categorie", back_populates='sources')
    tendances = relationship("Tendance", back_populates='source')


class Tendance(Base):
    __tablename__ = 'tendances'
    id = Column(Integer, primary_key=True, index=True)
    valeur = Column(Float, nullable=False)
    pays = Column(String(100), nullable=True)
    date_heure = Column(DateTime, default=datetime.utcnow, nullable=False)
    source_id = Column(Integer, ForeignKey('sources_api.id'), nullable=False)
    indicateur_id = Column(Integer, ForeignKey('indicateurs.id'), nullable=False)

    # une tendance appartient à un indicateur et à une source.
    indicateur = relationship("Indicateur", back_populates='tendances')
    source = relationship("SourceAPI", back_populates='tendances')
    commentaires = relationship("Commentaire", back_populates='tendance')

class Historique(Base):
    __tablename__ = 'historiques'
    id = Column(Integer, primary_key=True, index=True)
    valeur = Column(Float, nullable=False)
    pays = Column(String(100), nullable=True)
    date_heure = Column(DateTime, default=datetime.utcnow, nullable=False)
    indicateur_id = Column(Integer, ForeignKey('indicateurs.id'), nullable=False)
    indicateur = relationship("Indicateur", back_populates='historique')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    date_inscription = Column(DateTime, default=datetime.utcnow)
    commentaires = relationship("Commentaire", back_populates='user')


class Commentaire(Base):
    __tablename__ = 'commentaires'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    date_heure = Column(DateTime, default=datetime.utcnow, nullable=False)
    tendance_id = Column(Integer, ForeignKey('tendances.id'), nullable=False)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates='commentaires')
    tendance = relationship("Tendance", back_populates='commentaires')