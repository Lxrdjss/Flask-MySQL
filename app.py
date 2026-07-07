"""app.py - API Flask d'analyse de sentiments pour SocialMetrics AI."""

from flask import Flask, request, jsonify

from model import predict_scores
from db import insert_tweet, get_connection

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    """Vérifie que l'API et la base de données répondent."""
    try:
        conn = get_connection()
        conn.close()
        db_status = "ok"
    except Exception as e:
        db_status = f"erreur: {e}"
    return jsonify({"status": "ok", "database": db_status}), 200


@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Reçoit une liste de tweets et retourne leurs scores de sentiment.

    Requête attendue (JSON) :
        {"tweets": ["tweet1", "tweet2", ...]}

    Réponse (JSON) :
        {"tweet1": score1, "tweet2": score2, ...}
    """
    data = request.get_json(silent=True)

    if data is None or "tweets" not in data:
        return jsonify({"error": "Le corps de la requête doit contenir une clé 'tweets'."}), 400

    tweets = data["tweets"]

    if not isinstance(tweets, list):
        return jsonify({"error": "'tweets' doit être une liste de chaînes de caractères."}), 400

    if len(tweets) == 0:
        return jsonify({"error": "La liste de tweets est vide."}), 400

    if not all(isinstance(t, str) and t.strip() for t in tweets):
        return jsonify({"error": "Chaque tweet doit être une chaîne de caractères non vide."}), 400

    try:
        scores = predict_scores(tweets)
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 503
    except Exception as e:
        return jsonify({"error": f"Erreur lors de l'analyse : {e}"}), 500

    result = {tweet: round(float(score), 4) for tweet, score in zip(tweets, scores)}
    return jsonify(result), 200


@app.route("/tweets", methods=["POST"])
def add_tweet():
    """
    Ajoute un tweet annoté à la base (utile pour enrichir le dataset d'entraînement).

    Requête attendue (JSON) :
        {"text": "...", "positive": 0 ou 1, "negative": 0 ou 1}
    """
    data = request.get_json(silent=True)

    if data is None or "text" not in data:
        return jsonify({"error": "Le corps de la requête doit contenir 'text'."}), 400

    text = data["text"]
    positive = data.get("positive", 0)
    negative = data.get("negative", 0)

    if not isinstance(text, str) or not text.strip():
        return jsonify({"error": "'text' doit être une chaîne non vide."}), 400

    if positive not in (0, 1) or negative not in (0, 1):
        return jsonify({"error": "'positive' et 'negative' doivent valoir 0 ou 1."}), 400

    try:
        insert_tweet(text, positive, negative)
    except Exception as e:
        return jsonify({"error": f"Erreur lors de l'insertion : {e}"}), 500

    return jsonify({"message": "Tweet ajouté avec succès."}), 201


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
