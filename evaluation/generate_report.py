"""generate_report.py - Génère les matrices de confusion et les métriques du modèle.

Usage :
    python evaluation/generate_report.py

Produit :
    evaluation/confusion_positive.png
    evaluation/confusion_negative.png
    evaluation/metrics.txt
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
)

from model import train_model

OUT_DIR = os.path.dirname(__file__)


def plot_confusion(y_true, y_pred, labels, title, filename):
    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    fig, ax = plt.subplots(figsize=(5, 5))
    disp.plot(ax=ax, cmap="Blues", colorbar=False)
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, filename))
    plt.close(fig)
    return cm


def main():
    result = train_model()
    X_test = result["X_test"]
    clf_positive = result["clf_positive"]
    clf_negative = result["clf_negative"]
    ypos_test = result["ypos_test"]
    yneg_test = result["yneg_test"]

    ypos_pred = clf_positive.predict(X_test)
    yneg_pred = clf_negative.predict(X_test)

    cm_pos = plot_confusion(
        ypos_test, ypos_pred,
        labels=["Non positif", "Positif"],
        title="Matrice de confusion - Positif",
        filename="confusion_positive.png",
    )
    cm_neg = plot_confusion(
        yneg_test, yneg_pred,
        labels=["Non négatif", "Négatif"],
        title="Matrice de confusion - Négatif",
        filename="confusion_negative.png",
    )

    lines = []
    lines.append("=== Rapport d'évaluation du modèle de sentiment ===\n")

    lines.append("--- Classe POSITIVE ---")
    lines.append(f"Précision : {precision_score(ypos_test, ypos_pred, zero_division=0):.3f}")
    lines.append(f"Rappel    : {recall_score(ypos_test, ypos_pred, zero_division=0):.3f}")
    lines.append(f"F1-score  : {f1_score(ypos_test, ypos_pred, zero_division=0):.3f}")
    lines.append(f"Matrice de confusion :\n{cm_pos}\n")
    lines.append(classification_report(ypos_test, ypos_pred, zero_division=0))

    lines.append("--- Classe NEGATIVE ---")
    lines.append(f"Précision : {precision_score(yneg_test, yneg_pred, zero_division=0):.3f}")
    lines.append(f"Rappel    : {recall_score(yneg_test, yneg_pred, zero_division=0):.3f}")
    lines.append(f"F1-score  : {f1_score(yneg_test, yneg_pred, zero_division=0):.3f}")
    lines.append(f"Matrice de confusion :\n{cm_neg}\n")
    lines.append(classification_report(yneg_test, yneg_pred, zero_division=0))

    report_text = "\n".join(lines)
    with open(os.path.join(OUT_DIR, "metrics.txt"), "w") as f:
        f.write(report_text)

    print(report_text)
    print(f"\nGraphiques sauvegardés dans {OUT_DIR}/")


if __name__ == "__main__":
    main()
