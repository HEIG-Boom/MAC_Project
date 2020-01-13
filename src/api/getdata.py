#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Provides functions to retrieve data from RapidAPI's movie-database-imdb-alternative
"""
import os
import requests

# Constant values used for requests
url = "https://movie-database-imdb-alternative.p.rapidapi.com/"
headers = {
    'x-rapidapi-host': 'movie-database-imdb-alternative.p.rapidapi.com',
    'x-rapidapi-key': os.getenv('SERIES_API_TOKEN')
}


def get_series_by_name(search):
    querystring = {"page": "1", "r": "json", "type": "series", "s": "sherlock"}

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.text
