import asyncio
from collecteur.collecteur_worldbank import CollecteurWorldBank
from collecteur.collecteur_frankfurter import CollecteurFrankfurter
from collecteur.collecteur_oilprice import CollecteurOilPrice
from collecteur.collecteur_alphavantage import CollecteurAlphavantage
from collecteur.collecteur_fred import CollecteurFRED


async def main():

    # Alpha Vantage — Bourse
    print("\n Alpha Vantage — Bourse...")
    await CollecteurAlphavantage(source_id=8).collecter()
    # World Bank — Économie
    print("\n World Bank — Économie...")
    await CollecteurWorldBank(source_id=1).collecter()

        # World Bank — Environnement
    print("\n World Bank — Environnement...")
    await CollecteurWorldBank(source_id=2).collecter()

        # World Bank — Social
    print("\n World Bank — Social...")
    await CollecteurWorldBank(source_id=3).collecter()
    print("\n oil price energie ...")
    await CollecteurOilPrice(source_id = 4).collecter()
    print("\n oil price  finance...")
    await CollecteurOilPrice(source_id = 5).collecter()

    # Frankfurter — Finance (Taux de change)
    print("\n Frankfurter — Taux de change...")
    await CollecteurFrankfurter(source_id=6).collecter()

    # FRED — Finance (Taux directeurs)
    print("\n FRED — Taux directeurs...")
    await CollecteurFRED(source_id=7).collecter()


    print("\n Collecte terminée !")


asyncio.run(main())