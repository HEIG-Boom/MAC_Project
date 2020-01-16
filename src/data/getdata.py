#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Provides functions to retrieve data from RapidAPI's movie-database-imdb-alternative
"""
import os
import json
import requests

# Constants necessary values for requests to the series API
API_URL = "https://movie-database-imdb-alternative.p.rapidapi.com/"

HEADERS = {
    'x-rapidapi-host': 'movie-database-imdb-alternative.p.rapidapi.com',
    'x-rapidapi-key': os.getenv('SERIES_API_TOKEN')
}


def get_series_by_name(search):
    """Execute a GET request using the given search term and return a dict"""
    querystring = {"page": "1", "r": "json", "type": "series", "s": search}

    response = requests.request("GET", API_URL, headers=HEADERS, params=querystring)

    return json.loads(response.text)


def format_series(series):
    """Format a python dict into a readable format"""
    return series
