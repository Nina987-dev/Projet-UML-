from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import CategorieResponse
from services import categories as service

router = APIRouter(prefix="/categories", tags=["Categories"])
@router.get("/", response_model= list[CategorieResponse])
def get_all(db: Session = Depends(get_db)):
    return service.get_all(db)