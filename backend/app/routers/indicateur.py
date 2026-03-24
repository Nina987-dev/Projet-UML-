from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import IndicateurResponse
from services import indicateurs as service

router = APIRouter(prefix="/indicateurs", tags=["Indicateurs"])

@router.get("/categories/{category_id}", response_model=list[IndicateurResponse])
def get_by_categorie(category_id: int, db: Session = Depends(get_db)):
    return service.get_by_categorie(db, category_id)