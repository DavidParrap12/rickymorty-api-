"""Pasos 1 y 2: consumir la API y cargar la data cruda a MongoDB (Data Lake)."""
import requests
from pymongo import MongoClient, UpdateOne

URL = "https://rickandmortyapi.com/api/character"
MONGO_URI = "mongodb://localhost:27017"

col = MongoClient(MONGO_URI)["rickandmorty_dl"]["characters"]

url, total = URL, 0
while url:
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    data = r.json()
    ops = [UpdateOne({"id": c["id"]}, {"$set": c}, upsert=True) for c in data["results"]]
    col.bulk_write(ops)
    total += len(ops)
    print(f"Cargados {total} personajes...")
    url = data["info"]["next"]  # None cuando se acaba la paginación

print("Listo. Total en Mongo:", col.count_documents({}))
