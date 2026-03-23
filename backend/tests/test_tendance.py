from datetime import datetime

from services import categories as categorie_service
from services import indicateurs as indicateur_service
from services import tendances as tendance_service
from schemas import CategorieBase, IndicateurBase, TendanceBase
from models import Base, SourceAPI

class TestTendanceService:

    def test_create_retourne_tendance(self, db, source, indicateur_taux):
        t = tendance_service.create(
            db, TendanceBase(valeur=1.08, pays="France", source_id=source.id, indicateur_id=indicateur_taux.id)
        )
        assert t.id is not None
        assert t.valeur == 1.08
        assert t.pays == "France"

    def test_create_sans_pays(self, db, source, indicateur_taux):
        t = tendance_service.create(
            db, TendanceBase(valeur=0.85, source_id=source.id, indicateur_id=indicateur_taux.id)
        )
        assert t.pays is None

    def test_date_heure_auto_renseignee(self, db, source, indicateur_taux):
        t = tendance_service.create(
            db, TendanceBase(valeur=1.10, source_id=source.id, indicateur_id=indicateur_taux.id)
        )
        assert t.date_heure is not None
        assert isinstance(t.date_heure, datetime)

    def test_get_all_vide(self, db):
        assert tendance_service.get_all(db) == []

    def test_get_all_retourne_toutes(self, db, source, indicateur_taux):
        tendance_service.create(db, TendanceBase(valeur=1.08, pays="France", source_id=source.id, indicateur_id=indicateur_taux.id))
        tendance_service.create(db, TendanceBase(valeur=1.10, pays="Allemagne", source_id=source.id, indicateur_id=indicateur_taux.id))
        assert len(tendance_service.get_all(db)) == 2

    def test_get_by_id_existant(self, db, tendance_france):
        result = tendance_service.get_by_id(db, tendance_france.id)
        assert result is not None
        assert result.valeur == 1.08

    def test_get_by_id_inexistant(self, db):
        assert tendance_service.get_by_id(db, 9999) is None

    def test_get_by_indicateur(self, db, source, indicateur_taux, categorie_economie):
        autre_ind = indicateur_service.create(
            db, IndicateurBase(name="Inflation", category_id=categorie_economie.id)
        )
        tendance_service.create(db, TendanceBase(valeur=1.08, pays="France", source_id=source.id, indicateur_id=indicateur_taux.id))
        tendance_service.create(db, TendanceBase(valeur=1.10, pays="Espagne", source_id=source.id, indicateur_id=indicateur_taux.id))
        tendance_service.create(db, TendanceBase(valeur=2.5, pays="France", source_id=source.id, indicateur_id=autre_ind.id))

        resultats = tendance_service.get_by_indicateur(db, indicateur_taux.id)
        assert len(resultats) == 2
        assert all(t.indicateur_id == indicateur_taux.id for t in resultats)

    def test_get_by_indicateur_inexistant(self, db):
        assert tendance_service.get_by_indicateur(db, 9999) == []

    def test_get_by_pays(self, db, source, indicateur_taux):
        tendance_service.create(db, TendanceBase(valeur=1.08, pays="France", source_id=source.id, indicateur_id=indicateur_taux.id))
        tendance_service.create(db, TendanceBase(valeur=0.85, pays="France", source_id=source.id, indicateur_id=indicateur_taux.id))
        tendance_service.create(db, TendanceBase(valeur=1.20, pays="Allemagne", source_id=source.id, indicateur_id=indicateur_taux.id))

        resultats = tendance_service.get_by_pays(db, "France")
        assert len(resultats) == 2
        assert all(t.pays == "France" for t in resultats)

    def test_get_by_pays_inexistant(self, db):
        assert tendance_service.get_by_pays(db, "Narnia") == []

    def test_update_modifie_valeur(self, db, tendance_france, indicateur_taux):
        data = TendanceBase(valeur=1.15, pays="France", source_id=tendance_france.source_id, indicateur_id=indicateur_taux.id)
        updated = tendance_service.update(db, "France", indicateur_taux.id, data)
        assert updated is not None
        assert updated.valeur == 1.15

    def test_update_met_a_jour_date_heure(self, db, tendance_france, indicateur_taux):
        date_avant = tendance_france.date_heure
        data = TendanceBase(valeur=1.20, pays="France", source_id=tendance_france.source_id, indicateur_id=indicateur_taux.id)
        updated = tendance_service.update(db, "France", indicateur_taux.id, data)
        assert updated.date_heure >= date_avant

    def test_update_pays_inexistant_retourne_none(self, db, indicateur_taux, source):
        data = TendanceBase(valeur=1.20, pays="Narnia", source_id=source.id, indicateur_id=indicateur_taux.id)
        assert tendance_service.update(db, "Narnia", indicateur_taux.id, data) is None

    def test_update_ne_cree_pas_de_doublon(self, db, tendance_france, indicateur_taux):
        data = TendanceBase(valeur=1.20, pays="France", source_id=tendance_france.source_id, indicateur_id=indicateur_taux.id)
        tendance_service.update(db, "France", indicateur_taux.id, data)
        assert len(tendance_service.get_all(db)) == 1