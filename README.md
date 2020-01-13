# MAC - Projet

[![Build Status](https://dev.azure.com/heig-boom/MAC%20Project/_apis/build/status/HEIG-Boom.MAC_Project?branchName=master)](https://dev.azure.com/heig-boom/MAC%20Project/_build/latest?definitionId=5&branchName=master)

## Description

Pour le projet du cours Méthodes d’accès aux données, nous avons décidé de réaliser un outil qui permettra aux utilisateurs de garder un historique sur leurs séries visionnées.

Plus précisément, chaque utilisateur pourra sélectionner les séries qui l'intéressent et garder une trace des épisodes regardés dans une série donnée. Il pourra également aimer les épisodes regardés. L’outil permettra de récupérer une liste des séries les plus populaires du moment, selon plusieurs filtres.

Ces interactions seront faites via un bot Telegram. Plusieurs commandes permettront d'interagir avec la base de données des séries.

## Utiliser le bot

Dans Telegram, chercher le bot `@MacBotBotMacBot`, et lancer une conversation.

Les commandes suivantes sont alors utilisables :

- ...

## Setup pour le développement

1. Créer un bot à l'aide du BotFather et copier l'API Token.
2. Créer un fichier `env-file` dans le dossier `docker`.
3. Écrire dans ce fichier `TELEGRAM_TOKEN=<le token récupéré>`.
4. Se positionner dans le dossier `docker` et utiliser la commande `docker-compose up --build -d`.
5. Le bot est maintenant "en ligne".

## Déploiement

Azure pipelines s'occupe de mettre à jour le code sur le serveur distant, afin de s'assurer que le bot de production soit toujours disponible.

Le pipeline est composé d'un simple job qui exécute le script `docker/deploy.sh` sur la machine distante, redémarrant ainsi les containers qui servent l'application.
