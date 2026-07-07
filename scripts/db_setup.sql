-- db_setup.sql
-- Création de la base et de la table tweets pour SocialMetrics AI

CREATE DATABASE IF NOT EXISTS sentiment_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE sentiment_db;

-- Utilisateur dédié à l'application (à adapter en production)
CREATE USER IF NOT EXISTS 'sentiment_user'@'localhost' IDENTIFIED BY 'sentiment_pass';
GRANT ALL PRIVILEGES ON sentiment_db.* TO 'sentiment_user'@'localhost';
FLUSH PRIVILEGES;

CREATE TABLE IF NOT EXISTS tweets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    positive TINYINT(1) NOT NULL DEFAULT 0,
    negative TINYINT(1) NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Quelques données d'exemple (le vrai dataset s'importe avec scripts/load_dataset.py)
INSERT INTO tweets (text, positive, negative) VALUES
('Ce produit est incroyable, je le recommande !', 1, 0),
('Service client catastrophique, je suis très déçu.', 0, 1),
('Livraison rapide et emballage soigné, merci.', 1, 0),
('C''est nul, ça ne fonctionne pas du tout.', 0, 1);
