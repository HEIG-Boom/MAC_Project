#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Database class allowing to initialize the connection and execute operations easily
"""
import os
from pyArango.connection import *
from decorators.singleton import Singleton
from datetime import date
from data.graph import SeriesGraph

# Database constants
DB_URL = os.getenv("DB_HOST", "http://127.0.0.1:8529")
DB_PWD = os.getenv("ARANGO_PWD", "password")


@Singleton
class Database(object):
    """Singleton database class, linking to ArangoDB database"""

    def __init__(self):
        """Initialize the data connection"""
        db_name = "teleshows"

        conn = Connection(DB_URL, username="root", password=DB_PWD)

        # Create database if it doesn't exist
        if not conn.hasDatabase(db_name):
            conn.createDatabase(name=db_name)
            self.db = conn[db_name]
        else:
            self.db = conn[db_name]

        # Create vertices and edges collections if they don't exist
        if not self.db.hasCollection("Users"):
            self.db.createCollection(name="Users", className='Collection')
        if not self.db.hasCollection("Series"):
            self.db.createCollection(name="Series", className='Collection')
        if not self.db.hasCollection("Seasons"):
            self.db.createCollection(name="Seasons", className='Collection')
        if not self.db.hasCollection("Episodes"):
            self.db.createCollection(name="Episodes", className='Collection')
        if not self.db.hasCollection("Follows"):
            self.db.createCollection(name="Follows", className='Edges')
        if not self.db.hasCollection("Includes"):
            self.db.createCollection(name="Includes", className='Edges')
        if not self.db.hasCollection("Contains"):
            self.db.createCollection(name="Contains", className='Edges')
        if not self.db.hasCollection("HasSeen"):
            self.db.createCollection(name="HasSeen", className='Edges')

        # Create the graph
        if not self.db.hasGraph("SeriesGraph"):
            self.graph = self.db.createGraph("SeriesGraph")
        else:
            self.graph = self.db.graphs['SeriesGraph']

        # Set collection as object properties to be easily accessed
        self.users_col = self.db['Users']
        self.series_col = self.db['Series']
        self.seasons_col = self.db['Seasons']
        self.episodes_col = self.db['Episodes']
        self.follows_edges = self.db['Follows']
        self.includes_edges = self.db['Includes']
        self.contains_edges = self.db['Contains']
        self.has_seen_edges = self.db['HasSeen']

    def add_user(self, telegram_id, telegram_username):
        """Add the telegram user in the database"""
        # Check if the user is already in the database
        if str(telegram_id) in self.users_col:
            user = self.users_col[str(telegram_id)]

            # Check if the username has changed
            if user["username"] != telegram_username:
                user["username"] = telegram_username
                user.save()
        else:
            # Create the new user
            user = self.users_col.createDocument({
                "_key": str(telegram_id),
                "username": telegram_username
            })
            user.save()

    def add_series(self, imdb_id, title, year, poster_url, nb_season):
        """Add the series in the database"""
        # Check if the series is already in the database
        if imdb_id not in self.series_col:
            # Create the new show
            series = self.series_col.createDocument({
                "_key": imdb_id,
                "title": title,
                "year": year,
                "poster_url": poster_url
            })
            series.save()

            # Create all seasons and first episode for each of them
            for x in range(1, int(nb_season) + 1):
                season = self.seasons_col.createDocument({
                    "_key": imdb_id + '.' + str(x),
                    "number": x,
                    "description": "Season {} of the '{}' show".format(x, title)
                })
                season.save()

                # Link the season with the show
                self.graph.link('Includes', series, season, {})

                # Create the first episode for the current season
                episode = self.episodes_col.createDocument({
                    "_key": season['_key'] + '.1',
                    "number": 1,
                    "description": "First episode of the season {} of the '{}' show".format(x, title)
                })
                episode.save()

                # Link the episode with the season
                self.graph.link('Contains', season, episode, {})

        else:
            series = self.series_col[imdb_id]
        return series

    def follow_series(self, user, series):
        already_exist = self.check_if_exist("Follows", user, series)
        if not already_exist:
            self.graph.link('Follows', user, series, {"start_date": date.today()})
            return True
        else:
            return False

    def followed_series(self, user_id):
        user = self.users_col[user_id]

        aql = "FOR show IN Series FOR follow IN Follows FILTER follow.`_from` == \"{}\" AND follow.`_to` == show.`_id` RETURN show".format(user._id)
        results = self.db.AQLQuery(aql, rawResults=False, batchSize=100)
        return results

    def get_show_by_id(self, show_id):
        return self.series_col[show_id]

    def get_seasons_by_series_id(self, show_id):
        show = self.series_col[show_id]

        aql = "for season in Seasons for include in Includes filter include.`_from` == \"{}\" and include.`_to` == season.`_id` return season".format(show._id)
        results = self.db.AQLQuery(aql, rawResults=False, batchSize=100)
        return results

    def get_episodes_by_season_id(self, season_id):
        season = self.seasons_col[season_id]

        aql = "for episode in Episodes for contain in Contains filter contain.`_from` == \"{}\" and contain.`_to` == episode.`_id` return episode".format(season._id)
        results = self.db.AQLQuery(aql, rawResults=False, batchSize=100)
        return results

    def add_episode(self, episode_id):
        token = episode_id.split(".")

        # Get the show to add description to the new Episode
        show = self.series_col[token[0]]

        # Get the season of the show to link the new episode
        season = self.seasons_col[token[0] + '.' + token[1]]

        # Create the new Episode
        episode = self.episodes_col.createDocument({
            "_key": episode_id,
            "number": token[2],
            "description": "Episode n°{} of the season {} of the '{}' show".format(token[2], token[1], show.title)
        })
        episode.save()

        # Link the new episode to the season of the show
        self.graph.link('Contains', season, episode, {})

    def has_seen(self, user_id, episode_id):
        user = self.users_col[user_id]
        episode = self.episodes_col[episode_id]
        already_exist = self.check_if_exist("HasSeen", user, episode)
        if not already_exist:
            # Link the new episode to the season of the show
            self.graph.link('HasSeen', user, episode, {"date": date.today()})
            return True
        else:
            return False

    def get_progress(self, user_id, show_id):
        user = self.users_col[user_id]
        show = self.series_col[show_id]

        nb_seasons = len(self.get_seasons_by_series_id(show_id))

        # Init the dictionary with empty lists
        resultsDict = {}
        keys = range(1, nb_seasons + 1)
        for i in keys:
            resultsDict[i] = []

        aql = "for watched in HasSeen filter watched.`_from` == \"{}\" and watched.`_to` like \"%{}.%\" return watched".format(user._id, show._key)
        results = self.db.AQLQuery(aql, rawResults=False, batchSize=100)

        for result in results:
            token = result._to.split('.')
            resultsDict[int(token[1])].append(token[2])

        return resultsDict

    def check_if_exist(self, collectionName, fromElement, toElement):
        aql = "for link in {} filter link.`_from` == \"{}\" and link.`_to` == \"{}\" return link".format(collectionName, fromElement._id, toElement._id)
        results = self.db.AQLQuery(aql, rawResults=False, batchSize=100)
        return results

    def __str__(self):
        return 'Database connection object'
