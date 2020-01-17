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
            db = conn[db_name]
        else:
            db = conn[db_name]

        # Create vertices and edges collections if they don't exist
        if not db.hasCollection("Users"):
            db.createCollection(name="Users", className='Collection')
        if not db.hasCollection("Series"):
            db.createCollection(name="Series", className='Collection')
        if not db.hasCollection("Follows"):
            db.createCollection(name="Follows", className='Edges')

        # Create the graph
        if not db.hasGraph("SeriesGraph"):
            self.graph = db.createGraph("SeriesGraph")
        else:
            self.graph = db.graphs['SeriesGraph']

        self.users_col = db['Users']
        self.series_col = db['Series']
        self.follows_edges = db['Follows']

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

    def __str__(self):
        return 'Database connection object'
