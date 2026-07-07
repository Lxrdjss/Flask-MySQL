#!/bin/bash
# retrain_cron.sh - Wrapper pour lancer le réentraînement via cron.
# Adapter PROJECT_DIR au chemin réel du projet sur le serveur.

PROJECT_DIR="/opt/sentiment-api"
VENV_PATH="$PROJECT_DIR/venv/bin/activate"

cd "$PROJECT_DIR" || exit 1
source "$VENV_PATH"
python retrain.py >> "$PROJECT_DIR/retrain_cron.log" 2>&1
