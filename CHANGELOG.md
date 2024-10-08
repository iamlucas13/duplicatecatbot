# 📋 CHANGELOG

Tous les changements notables apportés à ce projet seront documentés dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
et ce projet adhère à [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 28-08-2024

### Ajouté
- Message indiquant l'exécution de la requête.
- Message de notification lorsqu'un utilisateur n'a pas la permission pour exécuter une commande.

### Modifié
- Mise à jour de la structure du projet pour une décomposition modulaire.

## [1.0.0] - 26-08-2024

### Ajouté
- Fonctionnalité de duplication complète des catégories, y compris les salons et les permissions.
- Commande `!duplicate_category <category_id>` pour dupliquer une catégorie entière.
- Commande `!duplicate_category_only <category_id>` pour dupliquer uniquement la catégorie sans les salons.
- Conservation des permissions lors de la duplication des catégories et des salons.
- **Restriction d'accès** : Les commandes du bot sont désormais réservées aux administrateurs.
- Documentation initiale avec `README.md`.

---

## Comment contribuer

- Pour soumettre des modifications, veuillez ouvrir une Pull Request avec une description claire de vos modifications.
- Assurez-vous que vos modifications suivent les conventions de versioning sémantique.
