import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

def init_db():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # On supprime TOUT pour repartir sur une base saine
                cur.execute("""
                    DROP TABLE IF EXISTS commentaires CASCADE;
                    DROP TABLE IF EXISTS tendances CASCADE;
                    DROP TABLE IF EXISTS historique CASCADE;
                    DROP TABLE IF EXISTS sources CASCADE;
                    DROP TABLE IF EXISTS indicateurs CASCADE;
                    DROP TABLE IF EXISTS categories CASCADE;
                    DROP TABLE IF EXISTS users CASCADE;
                """)

                cur.execute("CREATE TABLE categories (id SERIAL PRIMARY KEY, nom VARCHAR(100) UNIQUE NOT NULL);")

                cur.execute("""
                    CREATE TABLE indicateurs (
                        id SERIAL PRIMARY KEY, 
                        name VARCHAR(100) NOT NULL, 
                        unit VARCHAR(50), 
                        description TEXT, 
                        category_id INTEGER REFERENCES categories(id) ON DELETE CASCADE
                    );
                """)

                cur.execute("""
                    CREATE TABLE sources (
                        id SERIAL PRIMARY KEY, 
                        nom VARCHAR(100) NOT NULL, 
                        url TEXT, 
                        category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL
                    );
                """)

                cur.execute("""
                    CREATE TABLE tendances (
                        id SERIAL PRIMARY KEY, 
                        titre TEXT, 
                        description TEXT, 
                        valeur FLOAT, 
                        pays VARCHAR(100), 
                        url TEXT, 
                        source_id INTEGER REFERENCES sources(id), 
                        indicateur_id INTEGER REFERENCES indicateurs(id), 
                        date_publication TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)

                cur.execute("""
                    CREATE TABLE historique (
                        id SERIAL PRIMARY KEY, 
                        valeur FLOAT NOT NULL, 
                        pays VARCHAR(100), 
                        indicateur_id INTEGER REFERENCES indicateurs(id), 
                        date_heure TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)

                cur.execute("""
                    CREATE TABLE users (
                        id SERIAL PRIMARY KEY, 
                        name VARCHAR(100) NOT NULL, 
                        first_name VARCHAR(100) NOT NULL, 
                        email VARCHAR(255) UNIQUE NOT NULL, 
                        password VARCHAR(255) NOT NULL, 
                        date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)

                cur.execute("""
                    CREATE TABLE commentaires (
                        id SERIAL PRIMARY KEY, 
                        text TEXT NOT NULL, 
                        tendance_id INTEGER REFERENCES tendances(id) ON DELETE CASCADE, 
                        id_user INTEGER REFERENCES users(id) ON DELETE CASCADE, 
                        date_heure TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)

                # Insertion des données de base nécessaires
                cur.execute("INSERT INTO categories (nom) VALUES ('Actualités'), ('Finance'), ('Social'), ('Économie') ON CONFLICT DO NOTHING;")
                cur.execute("INSERT INTO indicateurs (name, category_id) SELECT 'Taux de change', id FROM categories WHERE nom='Économie';")
                
                conn.commit()
                print("Base de données réinitialisée avec succès")
    except Exception as e:
        print("Erreur d'initialisation :", e)

if __name__ == "__main__":
    init_db()