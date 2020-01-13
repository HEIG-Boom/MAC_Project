#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Handles all commands related to the manipulation of TV shows data
"""
from api.getdata import get_series_by_name


# TODO complete
def search_series(update, context):
    update.message.reply_text(get_series_by_name('lol'))
