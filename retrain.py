"""retrain.py - Réentraîne le modèle avec les données les plus récentes de la table tweets.

Destiné à être appelé par un cronjob (voir scripts/retrain_cron.sh).
"""

import logging
from datetime import datetime

from model import train_model

logging.basicConfig(
    filename="retrain.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def main():
    start = datetime.now()
    try:
        result = train_model()
        msg = f"Réentraînement réussi sur {result['n_samples']} tweets."
        print(msg)
        logging.info(msg)
    except Exception as e:
        msg = f"Échec du réentraînement : {e}"
        print(msg)
        logging.error(msg)
        raise
    finally:
        logging.info(f"Durée : {datetime.now() - start}")


if __name__ == "__main__":
    main()
