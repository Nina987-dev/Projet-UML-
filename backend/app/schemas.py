from pydantic import BaseModel
from datetime import datetime

class CategorieBase(BaseModel):
    name: str

class CategorieResponse(CategorieBase):
    id: int
    class Config:
        from_attributes = True

class IndicateurBase(BaseModel):
    name: str
    unit: str |None = None
    category_id: int
    description: str |None = None

class IndicateurResponse(IndicateurBase):
    id: int
    class Config:
        from_attributes = True

class SourceAPIBase(BaseModel):
    name: str
    url_base: str
    category_id: int

class SourceAPIResponse(SourceAPIBase):
    id: int
    class Config:
        from_attributes = True

class TendanceBase(BaseModel):
    valeur: float
    pays: str
    source_id: int
    indicateur_id: int
class TendanceResponse(TendanceBase):

    id              : int
    date_heure      : datetime

    indicateur_name : str | None = None
    indicateur_unit : str | None = None
    source_name : str | None = None
    class Config:
        from_attributes = True

class HistoriqueBase(BaseModel):
    valeur: float
    pays: str | None = None
    indicateur_id: int

class HistoriqueResponse(HistoriqueBase):
    id              : int
    date_heure      : datetime
    indicateur_name : str | None = None
    indicateur_unit : str | None = None
    source_name     : str | None = None
    class Config:
        from_attributes = True
class UserBase(BaseModel):
    name: str
    first_name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int

    date_inscription: datetime
    class Config:
        from_attributes = True
class CommentaireBase(BaseModel):
    text: str
    tendance_id: int
    id_user: int
class CommentaireResponse(CommentaireBase):
    id: int
    date_heure: datetime
    class Config:
        from_attributes = True
