"""Paso 3: conocer la estructura del documento."""
import json
from pymongo import MongoClient

col = MongoClient("mongodb://localhost:27017")["rickandmorty_dl"]["characters"]
doc = col.find_one({}, {"_id": 0})
print(json.dumps(doc, indent=2, ensure_ascii=False))
print("\nCampos:", list(doc.keys()))
print("Tipos:", {k: type(v).__name__ for k, v in doc.items()})
