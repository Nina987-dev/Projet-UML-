import asyncio
from collecteur.collecteur_worldbank import CollecteurWorldBank

async def main():
    collecteur = CollecteurWorldBank(source_id=1)
    await collecteur.collecter()
    print("✅ Collecte terminée !")

asyncio.run(main())