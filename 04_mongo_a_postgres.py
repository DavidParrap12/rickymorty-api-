"""Paso 7: transformar y cargar de Mongo (DL) a PostgreSQL (DWH)."""
import os
from typing import Any, Optional

import psycopg2
from pymongo import MongoClient
from pymongo.collection import Collection

PG_CONFIG: dict[str, Any] = {
    "host": os.getenv("PG_HOST", "localhost"),
    "dbname": os.getenv("PG_DB", "rickandmorty_dwh"),
    "user": os.getenv("PG_USER", "postgres"),
    "password": os.getenv("PG_PASSWORD", ""),
}
MONGO_URI = "mongodb://localhost:27017"


def id_from_url(url: Optional[str]) -> Optional[int]:
    """Saca el id numérico del final de una URL de la API."""
    if not url:
        return None
    return int(url.rstrip("/").split("/")[-1])


def main() -> None:
    col: Collection[dict[str, Any]] = MongoClient(MONGO_URI)["rickandmorty_dl"]["characters"]
    conn = psycopg2.connect(**PG_CONFIG)
    cur = conn.cursor()

    def upsert_location(loc: dict[str, Any]) -> Optional[int]:
        lid = id_from_url(loc.get("url"))
        if lid is None:  # origen/ubicación "unknown" no trae URL
            return None
        cur.execute(
            "INSERT INTO location (location_id, name, url) VALUES (%s, %s, %s) "
            "ON CONFLICT (location_id) DO NOTHING",
            (lid, loc["name"], loc["url"]),
        )
        return lid

    for c in col.find({}, {"_id": 0}):
        cur.execute(
            "INSERT INTO species (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
            (c["species"],),
        )
        cur.execute("SELECT species_id FROM species WHERE name = %s", (c["species"],))
        species_id = cur.fetchone()[0]  # type: ignore[index]

        origin_id = upsert_location(c["origin"])
        loc_id = upsert_location(c["location"])

        cur.execute(
            """
            INSERT INTO character
                (character_id, name, status, species_id, type, gender,
                 origin_id, location_id, image, created)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (character_id) DO NOTHING
            """,
            (c["id"], c["name"], c["status"], species_id, c["type"], c["gender"],
             origin_id, loc_id, c["image"], c["created"]),
        )

        for ep_url in c["episode"]:
            ep_id = id_from_url(ep_url)
            cur.execute(
                "INSERT INTO episode (episode_id) VALUES (%s) ON CONFLICT DO NOTHING",
                (ep_id,),
            )
            cur.execute(
                "INSERT INTO character_episode VALUES (%s, %s) ON CONFLICT DO NOTHING",
                (c["id"], ep_id),
            )

    conn.commit()
    cur.close()
    conn.close()
    print("Carga al DWH terminada.")


if __name__ == "__main__":
    main()