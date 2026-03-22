from fastapi import FastAPI
from database import engine, Base
import models

app = FastAPI(
    title="Trendflow",
    version="1.0.0"
)

#on crée les tables au démarrage

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"Plateforme de visualisation de données mondiales"}