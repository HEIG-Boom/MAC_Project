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
        if not self.db.hasCollection("Follows"):
            self.db.createCollection(name="Follows", className='Edges')

        # Create the graph
        if not self.db.hasGraph("SeriesGraph"):
            self.graph = self.db.createGraph("SeriesGraph")
        else:
            self.graph = self.db.graphs['SeriesGraph']

        self.users_col = self.db['Users']
        self.series_col = self.db['Series']
        self.follows_edges = self.db['Follows']

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

    def add_series(self, imdb_id, title, year, poster_url):
        """Add the series in the database"""
        # Check if the series is already in the database
        if imdb_id not in self.series_col:
            # Create the new user
            series = self.series_col.createDocument({
                "_key": imdb_id,
                "title": title,
                "year": year,
                "poster_url": poster_url
            })
            series.save()
        else:
            series = self.series_col[imdb_id]
        return series

    def follow_series(self, user, series):
        # TODO Check if the link already exists !
        self.graph.link('Follows', user, series, {"start_date": date.today()})

    def followed_series(self, user_id):
        user = self.users_col[user_id]

        aql = "FOR show IN Series FOR follow IN Follows FILTER follow.`_from` == \"{}\" AND follow.`_to` == show.`_id` RETURN show".format(user._id)
        results = self.db.AQLQuery(aql, rawResults=False, batchSize=100)
        return results

    def get_show_by_id(self, show_id):
        return self.series_col[show_id]

    def __str__(self):
        return 'Database connection object'
