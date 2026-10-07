# ETL Rick and Morty (API -> Mongo -> PostgreSQL)

1. `pip install -r requirements.txt`
2. Tener MongoDB y PostgreSQL corriendo.
3. `python 01_api_a_mongo.py`       -> Data Lake (Mongo)
4. `python 02_explorar_estructura.py`
5. `createdb rickandmorty_dwh` y `psql -d rickandmorty_dwh -f 03_esquema.sql`
6. Editar el password en `04_mongo_a_postgres.py` y ejecutarlo.
