# Requêtes pour le Collecteur 
INSERT_CATEGORY = """
    INSERT INTO categories (nom) 
    VALUES (%s) 
    ON CONFLICT (nom) DO UPDATE SET nom=EXCLUDED.nom 
    RETURNING id;
"""

INSERT_SOURCE = """
    INSERT INTO sources (nom, category_id) 
    VALUES (%s, %s) 
    ON CONFLICT DO NOTHING 
    RETURNING id;
"""

SELECT_SOURCE_ID = "SELECT id FROM sources WHERE nom = %s AND category_id = %s;"

INSERT_TENDANCE = """
    INSERT INTO tendances (titre, description, valeur, url, source_id, date_publication)
    VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
    RETURNING id;
"""

INSERT_HISTORIQUE = """
    INSERT INTO historique (valeur, indicateur_id, date_heure)
    VALUES (%s, (SELECT id FROM indicateurs WHERE category_id = %s LIMIT 1), CURRENT_TIMESTAMP);
"""

DELETE_OLD_TRENDS = "DELETE FROM tendances WHERE date_publication < NOW() - INTERVAL '%s hours';"

# Requêtes pour l'API (main.py)
GET_ALL_TRENDS = """
    SELECT t.id, t.titre, t.description, t.valeur, t.url, s.nom AS source, t.date_publication
    FROM tendances t
    JOIN sources s ON t.source_id = s.id
    ORDER BY t.date_publication DESC;
"""

GET_HISTORY_BY_CATEGORY = """
    SELECT h.date_heure, h.valeur, i.name 
    FROM historique h
    JOIN indicateurs i ON h.indicateur_id = i.id
    JOIN categories c ON i.category_id = c.id
    WHERE c.nom = %s
    ORDER BY h.date_heure ASC;
"""