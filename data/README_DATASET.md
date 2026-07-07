# Dataset — tweets_dataset.csv

## Origine
6000 tweets (3000 positifs, 3000 négatifs), équilibrés, extraits et adaptés à partir de
[French-Sentiment-Analysis-Dataset](https://github.com/gamebusterz/French-Sentiment-Analysis-Dataset)
(licence MIT), lui-même dérivé de **Sentiment140** (tweets en anglais traduits automatiquement
en français via Google Translate).

## Format
Colonnes : `text`, `positive` (0/1), `negative` (0/1).

## Limites à mentionner dans le rapport d'évaluation
- **Annotation faible ("distant supervision")** : dans Sentiment140, le sentiment n'est pas
  annoté par des humains mais déduit automatiquement des émoticônes présentes dans le tweet
  original (😀 → positif, 😞 → négatif). Cela introduit du bruit (un tweet peut contenir une
  émoticône positive tout en étant sarcastique, par exemple).
- **Traduction automatique** : le texte français est parfois maladroit ou grammaticalement
  incorrect, ce qui peut dégrader la qualité des features TF-IDF.
- **Biais de contenu** : les tweets datent de 2009 (culture, références, orthographe de
  l'époque), donc pas forcément représentatifs du langage actuel sur X.

## Charger le dataset
```bash
python scripts/load_dataset.py data/tweets_dataset.csv --replace
python model.py
```

## Pour aller plus loin
Pour un dataset annoté manuellement et 100% français (meilleure qualité, mais volumétrie plus
faible), voir aussi le corpus **Canéphore** (10 000 tweets français annotés manuellement,
événement Miss France 2012) : https://github.com/ressources-tal/canephore.
