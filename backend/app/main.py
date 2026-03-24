from fastapi import FastAPI
from database import engine, Base
import models
from routers import categories, indicateur, tendances
app = FastAPI(
    title="Trendflow",
    version="1.0.0"
)

#on crée les tables au démarrage
Base.metadata.create_all(bind=engine)

# on branche les routers
app.include_router(categories.router)
app.include_router(indicateur.router)
app.include_router(tendances.router)


@app.get("/")
def read_root():
    return {"Plateforme de visualisation de données mondiales"}