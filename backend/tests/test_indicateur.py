from services import categories as categorie_service
from services import indicateurs as indicateur_service
from services import tendances as tendance_service
from schemas import CategorieBase, IndicateurBase, TendanceBase
from models import Base, SourceAPI

class TestIndicateurService:

    def test_create_retourne_indicateur(self, db, categorie_economie):
        ind = indicateur_service.create(
            db, IndicateurBase(name="PIB", unit="USD", category_id=categorie_economie.id)
        )
        assert ind.id is not None
        assert ind.name == "PIB"
        assert ind.unit == "USD"
        assert ind.category_id == categorie_economie.id

    def test_create_sans_unit_ni_description(self, db, categorie_economie):
        ind = indicateur_service.create(
            db, IndicateurBase(name="Chômage", category_id=categorie_economie.id)
        )
        assert ind.unit is None
        assert ind.description is None

    def test_get_all_vide(self, db):
        assert indicateur_service.get_all(db) == []

    def test_get_all_retourne_tous(self, db, categorie_economie):
        indicateur_service.create(db, IndicateurBase(name="PIB", category_id=categorie_economie.id))
        indicateur_service.create(db, IndicateurBase(name="Inflation", category_id=categorie_economie.id))
        assert len(indicateur_service.get_all(db)) == 2

    def test_get_by_id_existant(self, db, indicateur_taux):
        result = indicateur_service.get_by_id(db, indicateur_taux.id)
        assert result is not None
        assert result.name == "Taux de change"

    def test_get_by_id_inexistant(self, db):
        assert indicateur_service.get_by_id(db, 9999) is None

    def test_get_by_categorie_retourne_les_bons(self, db, categorie_economie):
        cat2 = categorie_service.create(db, CategorieBase(name="Social"))
        indicateur_service.create(db, IndicateurBase(name="PIB", category_id=categorie_economie.id))
        indicateur_service.create(db, IndicateurBase(name="Chômage", category_id=categorie_economie.id))
        indicateur_service.create(db, IndicateurBase(name="Tweets", category_id=cat2.id))

        resultats = indicateur_service.get_by_categorie(db, categorie_economie.id)
        assert len(resultats) == 2
        assert {i.name for i in resultats} == {"PIB", "Chômage"}

    def test_get_by_categorie_inexistante_retourne_vide(self, db):
        assert indicateur_service.get_by_categorie(db, 9999) == []