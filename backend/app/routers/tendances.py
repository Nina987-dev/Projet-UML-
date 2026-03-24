from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import TendanceResponse
from services import tendances as service

router = APIRouter(prefix="/tendances", tags=["Tendances"])


@router.get("/categories/{category_id}", response_model=list[TendanceResponse])
def get_by_categorie(category_id: int, db: Session = Depends(get_db)):
    resultats = service.get_by_category(db, category_id)
    return [
        TendanceResponse(
            id              = t.id,
            valeur          = t.valeur,
            pays            = t.pays,
            date_heure      = t.date_heure,
            indicateur_id   = t.indicateur_id,
            source_id       = t.source_id,
            indicateur_name = i.name,
            indicateur_unit = i.unit,
            source_name     = None
        )
        for t, i in resultats
    ]


@router.get("/indicateur/{indicateur_id}", response_model=list[TendanceResponse])
def get_by_indicateur(indicateur_id: int, db: Session = Depends(get_db)):
    resultats = service.get_by_indicateur(db, indicateur_id)
    return [
        TendanceResponse(
            id              = t.id,
            valeur          = t.valeur,
            pays            = t.pays,
            date_heure      = t.date_heure,
            indicateur_id   = t.indicateur_id,
            source_id       = t.source_id,
            indicateur_name = i.name,
            indicateur_unit = i.unit,
            source_name     = s.name
        )
        for t, i, s in resultats
    ]
