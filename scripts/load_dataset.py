"""load_dataset.py - Charge un CSV annoté (colonnes: text, positive, negative) dans la table tweets.

Usage :
    python scripts/load_dataset.py data/tweets_dataset.csv
    python scripts/load_dataset.py data/tweets_dataset.csv --replace   # vide la table avant import
"""

import sys
import os
import csv
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from db import get_connection


def load_csv(path, replace=False):
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [(r["text"], int(r["positive"]), int(r["negative"])) for r in reader]

    conn = get_connection()
    try:
        cursor = conn.cursor()
        if replace:
            cursor.execute("DELETE FROM tweets")
        cursor.executemany(
            "INSERT INTO tweets (text, positive, negative) VALUES (%s, %s, %s)", rows
        )
        conn.commit()
        cursor.close()
    finally:
        conn.close()

    print(f"{len(rows)} tweets chargés depuis {path}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", help="Chemin vers le fichier CSV (colonnes: text, positive, negative)")
    parser.add_argument("--replace", action="store_true", help="Vide la table tweets avant l'import")
    args = parser.parse_args()

    load_csv(args.csv_path, replace=args.replace)
