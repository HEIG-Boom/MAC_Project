#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Handles all commands related to the manipulation of TV shows data
"""
from data.getdata import get_series_by_name, format_series


def search_series(update, context):
    """Respond to user with a list of series corresponding to its search terms"""
    if len(context.args) >= 1:
        search = ' '.join(context.args)

        update.message.reply_text(format_series(get_series_by_name(search)))
    else:
        update.message.reply_text("Please provide a search term to the command.")
