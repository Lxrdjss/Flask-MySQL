"""model.py - Modèle de sentiment basé sur TF-IDF + LogisticRegression.

Deux classifieurs binaires partagent le même vectoriseur TF-IDF :
- clf_positive : prédit la probabilité que le tweet soit positif
- clf_negative : prédit la probabilité que le tweet soit négatif

Le score final renvoyé par l'API est :
    score = P(positive) - P(negative)   -> compris entre -1 et 1
"""

import os
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from db import fetch_all_tweets

MODEL_DIR = os.path.join(os.path.dirname(__file__), "artifacts")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "vectorizer.joblib")
CLF_POS_PATH = os.path.join(MODEL_DIR, "clf_positive.joblib")
CLF_NEG_PATH = os.path.join(MODEL_DIR, "clf_negative.joblib")


def train_model(test_size=0.2, random_state=42):
    """Entraîne le modèle sur les données de la table tweets et sauvegarde les artefacts.

    Retourne un dict avec les jeux de test (pour l'évaluation / matrices de confusion).
    """
    rows = fetch_all_tweets()
    if len(rows) < 4:
        raise ValueError("Pas assez de données annotées pour entraîner le modèle (minimum 4 lignes).")

    texts = [r["text"] for r in rows]
    y_pos = np.array([r["positive"] for r in rows])
    y_neg = np.array([r["negative"] for r in rows])

    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X = vectorizer.fit_transform(texts)

    X_train, X_test, ypos_train, ypos_test, yneg_train, yneg_test = train_test_split(
        X, y_pos, y_neg, test_size=test_size, random_state=random_state
    )

    clf_positive = LogisticRegression(max_iter=1000)
    clf_positive.fit(X_train, ypos_train)

    clf_negative = LogisticRegression(max_iter=1000)
    clf_negative.fit(X_train, yneg_train)

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    joblib.dump(clf_positive, CLF_POS_PATH)
    joblib.dump(clf_negative, CLF_NEG_PATH)

    return {
        "X_test": X_test,
        "ypos_test": ypos_test,
        "yneg_test": yneg_test,
        "clf_positive": clf_positive,
        "clf_negative": clf_negative,
        "n_samples": len(rows),
    }


def _load_artifacts():
    if not (os.path.exists(VECTORIZER_PATH) and os.path.exists(CLF_POS_PATH) and os.path.exists(CLF_NEG_PATH)):
        raise FileNotFoundError(
            "Modèle non entraîné. Lancez `python model.py` ou `python retrain.py` d'abord."
        )
    vectorizer = joblib.load(VECTORIZER_PATH)
    clf_positive = joblib.load(CLF_POS_PATH)
    clf_negative = joblib.load(CLF_NEG_PATH)
    return vectorizer, clf_positive, clf_negative


def predict_scores(tweets):
    """Calcule un score de sentiment entre -1 et 1 pour chaque tweet de la liste."""
    if not tweets:
        return []

    vectorizer, clf_positive, clf_negative = _load_artifacts()
    X = vectorizer.transform(tweets)

    proba_pos = clf_positive.predict_proba(X)[:, 1]
    proba_neg = clf_negative.predict_proba(X)[:, 1]

    scores = proba_pos - proba_neg
    return np.clip(scores, -1, 1).tolist()


if __name__ == "__main__":
    result = train_model()
    print(f"Modèle entraîné sur {result['n_samples']} tweets. Artefacts sauvegardés dans {MODEL_DIR}/")
