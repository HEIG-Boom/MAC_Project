#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Data models to easily instantiate collection elements
"""


class User(object):
    def __init__(self, telegram_id, telegram_username):
        self.telegram_id = telegram_id
        self.telegram_username = telegram_username


class Series(object):
    def __init__(self, id, title, year, poster_url):
        self.id = id
        self.title = title
        self.year = year
        self.poster_url = poster_url