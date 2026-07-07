"""db.py - Gestion de la connexion à la base MySQL et accès aux données tweets."""

import os
import mysql.connector
from mysql.connector import Error


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "sentiment_db"),
}


def get_connection():
    """Ouvre et retourne une connexion MySQL."""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        raise ConnectionError(f"Impossible de se connecter à MySQL : {e}")


def fetch_all_tweets():
    """Récupère tous les tweets annotés (text, positive, negative)."""
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT text, positive, negative FROM tweets")
        rows = cursor.fetchall()
        cursor.close()
        return rows
    finally:
        conn.close()


def insert_tweet(text, positive, negative):
    """Insère un tweet annoté dans la table tweets."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tweets (text, positive, negative) VALUES (%s, %s, %s)",
            (text, int(positive), int(negative)),
        )
        conn.commit()
        cursor.close()
    finally:
        conn.close()
