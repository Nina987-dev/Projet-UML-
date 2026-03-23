import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, SourceAPI
from schemas import CategorieBase, IndicateurBase, TendanceBase
from services import categories as categorie_service
from services import indicateurs as indicateur_service
from services import tendances as tendance_service

@pytest.fixture(scope="function")
def db():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def categorie_economie(db):
    return categorie_service.create(db, CategorieBase(name="Économie"))


@pytest.fixture
def source(db, categorie_economie):
    src = SourceAPI(name="TestAPI", url_base="https://api.test.com", category_id=categorie_economie.id)
    db.add(src)
    db.commit()
    db.refresh(src)
    return src


@pytest.fixture
def indicateur_taux(db, categorie_economie):
    return indicateur_service.create(
        db,
        IndicateurBase(name="Taux de change", unit="EUR/USD", category_id=categorie_economie.id),
    )


@pytest.fixture
def tendance_france(db, source, indicateur_taux):
    return tendance_service.create(
        db,
        TendanceBase(valeur=1.08, pays="France", source_id=source.id, indicateur_id=indicateur_taux.id),
    )
 