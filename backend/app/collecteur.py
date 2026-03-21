import os
import httpx
import psycopg2
import queries
from dotenv import load_dotenv
from abc import ABC, abstractmethod

load_dotenv()

class SmartCollector(ABC):
    def __init__(self):
        self.db_params = {
            "dbname": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT")
        }

    def _get_conn(self):
        return psycopg2.connect(**self.db_params)

    def fetch(self, url, params=None):
        with httpx.Client() as client:
            res = client.get(url, params=params)
            res.raise_for_status()
            return res.json()

    @abstractmethod
    def collect(self):
        pass

    def cleanup_realtime_only(self, hours=24):
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(queries.DELETE_OLD_TRENDS, (hours,))
            conn.commit()

    def save_data(self, category_name, source_name, data_list):
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(queries.INSERT_CATEGORY, (category_name,))
                cat_id = cur.fetchone()[0]

                cur.execute(queries.INSERT_SOURCE, (source_name, cat_id))
                row = cur.fetchone()
                
                if not row:
                    cur.execute(queries.SELECT_SOURCE_ID, (source_name, cat_id))
                    src_id = cur.fetchone()[0]
                else:
                    src_id = row[0]

                for item in data_list:
                    cur.execute(queries.INSERT_TENDANCE, (
                        item.get('titre'), item.get('desc'), 
                        item.get('val'), item.get('url'), src_id
                    ))
                    
                    if item.get('val') is not None:
                        cur.execute(queries.INSERT_HISTORIQUE, (item.get('val'), cat_id))
            conn.commit()

class NewsPlugin(SmartCollector):
    def collect(self, query="économie"):
        params = {"q": query, "apiKey": os.getenv("NEWS_API_KEY"), "language": "fr"}
        data = self.fetch("https://newsapi.org/v2/everything", params)
        articles = data.get('articles', [])[:5]
        formatted = [{"titre": a.get('title'), "desc": a.get('description'), "url": a.get('url'), "val": None} for a in articles]
        self.save_data("Social", "NewsAPI", formatted)

class FinancePlugin(SmartCollector):
    def collect(self, from_symbol="EUR", to_symbol="USD"):
        params = {"function": "CURRENCY_EXCHANGE_RATE", "from_currency": from_symbol, "to_currency": to_symbol, "apikey": os.getenv("ALPHA_VANTAGE_KEY")}
        data = self.fetch("https://www.alphavantage.co/query", params)
        rate = data.get("Realtime Currency Exchange Rate", {}).get("5. Exchange Rate")
        if rate:
            formatted = [{"titre": f"Parité {from_symbol}/{to_symbol}", "desc": "Taux de change", "val": float(rate), "url": None}]
            self.save_data("Économie", "AlphaVantage", formatted)

if __name__ == "__main__":
    c = NewsPlugin()
    c.cleanup_realtime_only(24)
    c.collect("mondial")
    FinancePlugin().collect("EUR", "USD")
