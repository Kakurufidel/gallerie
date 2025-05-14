Cahier des Charges : Plateforme de Gestion Commerçants-Clients

Projet : Système d'orientation des clients vers les commerçants & gestion financière de galerie
1. Contexte

Objectif :

    Orienter les clients vers les commerçants proposant un produit spécifique.

    Gérer la finance d'une galerie commerciale (loyers, taxes, chiffre d'affaires).

Public Cible :

    Clients : Cherchent des produits en galerie.

    Commerçants : Vendeurs avec inventaire.

    Administrateurs : Gestion de la galerie.

2. Fonctionnalités Implémentées (MVP Actuel)
A. Gestion des Utilisateurs

    Rôles :

        Client : Peut rechercher des produits.

        Commerçant : Gère ses produits/chiffre d'affaires.

        Admin : Accès complet.

    Inscription :

        Commerçant : SIRET + validation manuelle (admin).

        Client : Email + mot de passe.

B. Gestion des Commerçants

    Profil Commerçant :

        Enseigne, SIRET, horaires d'ouverture (JSON).

        Statut actif/inactif.

    Produits :

        Catégories (alimentation, habillement...).

        Gestion de stock avec alertes.

        Prix HT/TTC (taux de TVA configurables).

C. Transactions & Finance

    Ventes :

        Lien produit-client avec montant automatique.

        Historique des transactions.

    Reporting :

        Chiffre d'affaires par période.

        Calcul automatique des loyers (surface × tarif).

D. Administration

    Backoffice Django Admin :

        Tableaux de bord personnalisés.

        Actions groupées (désactivation massive).

3. Architecture Technique
Backend (Django/PostgreSQL)

    Modèles Principaux :
    Diagram
    Code

    Services Clés :

        StockManager : Gestion transactionnelle du stock.

        MerchantReporting : Analytics financiers.

Fichiers Critiques
Fichier	Description
users/models.py	Rôles utilisateurs et auth.
commercants/models.py	Produits, transactions, règles métier.
commercants/services.py	Logique complexe (ventes, calculs).
4. Workflows Métier
Inscription Commerçant
Diagram
Code
Processus de Vente

    Client recherche un produit.

    Système vérifie le stock et le prix.

    Transaction enregistrée avec lien client-commerçant.

5. Règles Métier

    Validation SIRET : 14 chiffres obligatoires.

    Stock : Ne peut pas être négatif (CheckConstraint).

    Commerçant Inactif :

        Ses produits ne sont pas visibles.

        Impossible de réaliser des ventes.

6. Sécurité

    Authentification : JWT (Tokens).

    Permissions :

        Seuls les commerçants peuvent modifier leurs produits.

        Les admins voient tous les données.

7. Évolutions Futures (Backlog)
Priorité	Fonctionnalité
Haute	API REST pour le frontend mobile/web
Moyenne	Système de notifications (stocks, paiements)
Basse	Intégration Stripe pour paiements en ligne
8. Livrables Actuels

    Code Source :

        Modèles Django complets avec logique métier.

        Services pour les opérations critiques.

    Admin :

        Interface de gestion des commerçants/produits.

    Documentation :

        Schémas UML et workflows.

9. Prérequis Techniques

    Stack :

        Python 3.10+, Django 4.2, PostgreSQL (avec PostGIS).

    Outils :

        Docker (pour le déploiement).

        Celery (pour les tâches asynchrones futures).

10. Contacts

    Porteur de Projet : [Votre Nom]

    Équipe Technique : [Noms/Rôles]

Version : 1.0
Date : [Date de Rédaction]

Ce document sert de référence pour :

    L'équipe de développement.

    Les parties prenantes (investisseurs, commerciaux).

    Le pilotage des évolutions futures.
