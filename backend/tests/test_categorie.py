import pytest
from sqlalchemy.exc import IntegrityError

from services import categories as categorie_service
from services import indicateurs as indicateur_service
from services import tendances as tendance_service
from schemas import CategorieBase, IndicateurBase, TendanceBase
from models import Base, SourceAPI


class TestCategorieService:

    def test_create_retourne_objet_avec_id(self, db):
        cat = categorie_service.create(db, CategorieBase(name="Finance"))
        assert cat.id is not None
        assert cat.name == "Finance"

    def test_create_plusieurs_categories(self, db):
        categorie_service.create(db, CategorieBase(name="Finance"))
        categorie_service.create(db, CategorieBase(name="Social"))
        assert len(categorie_service.get_all(db)) == 2

    def test_get_all_vide(self, db):
        assert categorie_service.get_all(db) == []

    def test_get_all_retourne_toutes(self, db):
        categorie_service.create(db, CategorieBase(name="Finance"))
        categorie_service.create(db, CategorieBase(name="Social"))
        categorie_service.create(db, CategorieBase(name="Politique"))
        assert len(categorie_service.get_all(db)) == 3

    def test_get_by_id_existant(self, db, categorie_economie):
        result = categorie_service.get_category(db, categorie_economie.id)
        assert result is not None
        assert result.name == "Économie"

    def test_get_by_id_inexistant_retourne_none(self, db):
        assert categorie_service.get_category(db, 9999) is None

    def test_create_nom_unique(self, db):
        categorie_service.create(db, CategorieBase(name="Finance"))
        db.rollback()
        with pytest.raises(IntegrityError):
            categorie_service.create(db, CategorieBase(name="Finance"))