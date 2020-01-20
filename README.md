# MAC - Projet

[![Build Status](https://dev.azure.com/heig-boom/MAC%20Project/_apis/build/status/HEIG-Boom.MAC_Project?branchName=master)](https://dev.azure.com/heig-boom/MAC%20Project/_build/latest?definitionId=5&branchName=master)

## Description

Pour le projet du cours Méthodes d’accès aux données, nous avons décidé de réaliser un outil qui permettra aux utilisateurs de garder un historique sur leurs séries visionnées.

Plus précisément, chaque utilisateur pourra sélectionner les séries qui l'intéressent et garder une trace des épisodes regardés dans une série donnée. Il pourra également aimer les épisodes regardés. L’outil permettra de récupérer une liste des séries les plus populaires du moment, selon plusieurs filtres.

Ces interactions seront faites via un bot Telegram. Plusieurs commandes permettront d'interagir avec la base de données des séries.

## Utiliser le bot

Dans Telegram, chercher le bot `@TeleShows_Bot`, et lancer une conversation.

Les commandes suivantes sont alors utilisables (aide disponible avec la commande `/help`) :

- `/start` : start the bot 
- `/help` : get info on how to use the bot
- `/follow` : Search series that contain the term you specified after the command
- `/followed` : Display the shows you follow and mark an episode as seen
- `/progres` : See your progress in terms of episodes
- `/friends` : Find the users that have the most series in common with you

Pour les admins, l'interface ArangoDB en ligne est accessible à [cette addresse](http://teleshows.travelbook.beer:8529).

## Setup pour le développement

1. Créer un bot à l'aide du BotFather et copier l'API Token.
2. Nous utilisons [cette API](https://rapidapi.com/imdb/api/movie-database-imdb-alternative/endpoints) afin de livrer des données riches et actuelles aux utilisateurs.
3. Créer un fichier `.env` dans le dossier `docker`.
4. Remplir ce fichier avec les variables nécessaires au fonctionnement du bot :
    - `TELEGRAM_TOKEN=<le token récupéré>`
    - `SERIES_API_TOKEN=<votre token pour l'api de séries>`
    - `DB_HOST=http://db:8529`
    - `ARANGO_PWD=<votre mot de passe root pour la donnée>`
5. Se positionner dans le dossier `docker` et utiliser la commande `docker-compose up --build -d`.
6. Le bot est maintenant "en ligne".
7. Vous pouvez accéder à l'interface de la base de données à l'addresse [http://localhost:8529](http://localhost:8529) avec l'utilisateur `root` et le mot de passe précédemment défini.

## Déploiement

Azure pipelines s'occupe de mettre à jour le code sur le serveur distant, afin de s'assurer que le bot de production soit toujours disponible.

Le pipeline est composé d'un simple job qui exécute le script `docker/deploy.sh` sur la machine distante, redémarrant ainsi les containers qui servent l'application.
