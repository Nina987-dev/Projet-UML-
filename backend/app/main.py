from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os
from dotenv import load_dotenv
import queries

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

@app.get("/tendances")
def get_tendances():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(queries.GET_ALL_TRENDS)
                rows = cur.fetchall()
                
                return [
                    {
                        "id": r[0], 
                        "titre": r[1], 
                        "description": r[2], 
                        "valeur": r[3], 
                        "url": r[4], 
                        "source": r[5], 
                        "date": r[6]
                    } for r in rows
                ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/historique/{categorie}")
def get_historique(categorie: str):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(queries.GET_HISTORY_BY_CATEGORY, (categorie,))
                rows = cur.fetchall()
                return [{"date": r[0], "valeur": r[1], "indicateur": r[2]} for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
