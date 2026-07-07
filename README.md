# SocialMetrics AI — API d'Analyse de Sentiments

API Flask qui évalue le sentiment de tweets (score entre -1 et 1) à l'aide d'un modèle
de régression logistique entraîné sur des données stockées dans MySQL.

## Installation

```bash
git clone <url-du-repo>
cd sentiment-api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Base de données

```bash
mysql -u root -p < scripts/db_setup.sql
```

Variables d'environnement (optionnelles, valeurs par défaut entre parenthèses) :

```bash
export DB_HOST=localhost      # (localhost)
export DB_USER=root           # (root)
export DB_PASSWORD=motdepasse # ("")
export DB_NAME=sentiment_db   # (sentiment_db)
```

### Charger le dataset annoté

Un dataset de 6000 tweets (3000 positifs / 3000 négatifs) est fourni dans `data/tweets_dataset.csv`
(voir `data/README_DATASET.md` pour son origine et ses limites).

```bash
python scripts/load_dataset.py data/tweets_dataset.csv --replace
```

### Entraîner le modèle une première fois

```bash
python model.py
```

### Lancer l'API

```bash
python app.py
```

L'API écoute sur `http://localhost:5000`.

## Utilisation de l'API

### POST /analyze

Requête :

```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"tweets": ["J'\''adore ce produit !", "Service catastrophique."]}'
```

Réponse :

```json
{
  "J'adore ce produit !": 0.82,
  "Service catastrophique.": -0.75
}
```

Erreurs gérées : liste vide (400), champ `tweets` manquant ou mal formé (400),
modèle non entraîné (503).

### POST /tweets

Ajoute un tweet annoté au dataset d'entraînement :

```bash
curl -X POST http://localhost:5000/tweets \
  -H "Content-Type: application/json" \
  -d '{"text": "Bonne expérience globale.", "positive": 1, "negative": 0}'
```

### GET /health

Vérifie que l'API et la base de données répondent.

## Réentraînement automatique

Le script `retrain.py` réentraîne le modèle avec les données actuelles de la table `tweets`.

Réentraînement manuel :

```bash
python retrain.py
```

### Automatisation via cron (hebdomadaire)

1. Adapter `PROJECT_DIR` dans `scripts/retrain_cron.sh`.
2. Ajouter la ligne suivante à votre crontab (`crontab -e`) pour un réentraînement chaque
   lundi à 3h du matin :

```cron
0 3 * * 1 /opt/sentiment-api/scripts/retrain_cron.sh
```

Les logs sont écrits dans `retrain.log` et `retrain_cron.log`.

## Rapport d'évaluation

```bash
python evaluation/generate_report.py
```

Génère `evaluation/confusion_positive.png`, `evaluation/confusion_negative.png` et
`evaluation/metrics.txt` (précision, rappel, F1-score par classe).

## Structure du projet

```
sentiment-api/
├── app.py                  # API Flask
├── model.py                 # Entraînement et prédiction (TF-IDF + LogisticRegression)
├── db.py                    # Connexion et accès MySQL
├── retrain.py                # Script de réentraînement
├── requirements.txt
├── scripts/
│   ├── db_setup.sql          # Création base + table + données d'exemple
│   └── retrain_cron.sh       # Wrapper cron
└── evaluation/
    └── generate_report.py    # Génération des matrices de confusion et métriques
```
