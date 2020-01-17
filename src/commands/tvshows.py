#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Handles all commands related to the manipulation of TV shows data
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from data.series_api import get_series_by_name, get_series_by_id
from data.database import Database
from commands.utils import build_menu


def search_series(update, context):
    """Respond to user with a list of series corresponding to its search terms"""
    # Make sure the user provided a search term
    if len(context.args) >= 1:
        # Join search term tokens
        search = ' '.join(context.args)

        # Search for the series in API
        series = get_series_by_name(search)

        # Check response state
        if series["Response"] == "False":
            # Send error message
            update.message.reply_text("Oups! {}".format(series["Error"]))
        else:
            series = series["Search"]
            # Generate button list
            button_list = [InlineKeyboardButton("{} ({})".format(show["Title"], show["Year"]),
                                                callback_data=show["imdbID"]) for show in series]
            button_list.append(InlineKeyboardButton("None of those", callback_data="cancel"))

            # Create button menu
            reply_markup = InlineKeyboardMarkup(build_menu(button_list, 1))

            # Ask user to choose a show
            update.message.reply_text('Do you want to follow one of these series?', reply_markup=reply_markup)
    else:
        update.message.reply_text("Please provide a search term to the command.")


def handle_button(update, context):
    """Handle responses from the user when clicking menu buttons"""
    query = update.callback_query

    if query.data == "cancel":
        query.edit_message_text(text="Canceled")
    else:
        # Get details about the series
        show_details = get_series_by_id(query.data)

        db = Database.instance()
        # Create the series document
        series = db.add_series(show_details["imdbID"], show_details["Title"], show_details["Year"], show_details["Poster"])

        # Get the user document
        user_id = update.callback_query.message.chat.id
        user = db.users_col[user_id]

        # Create an edge between the documents
        db.follow_series(user, series)

        # Send success message
        text = "You are now following *{}*[.]({})".format(show_details["Title"], show_details["Poster"])
        query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN)
