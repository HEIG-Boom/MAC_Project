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
            update.message.reply_text("Do you want to follow one of these series?", reply_markup=reply_markup)
    else:
        update.message.reply_text("Please provide a search term to the command.")


def followed_series(update, context):
    user_id = update.message.chat.id

    db = Database.instance()
    series = db.followed_series(user_id)

    button_list = [InlineKeyboardButton("{} ({})".format(show["title"], show["year"]),
                                        callback_data="getSeasons" + show["_key"]) for show in series]
    # Create button menu
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, 1))

    # Ask user to choose a show
    if series:
        update.message.reply_text("You are following these series :", reply_markup=reply_markup)
    else:
        update.message.reply_text("It seems that you don't follow any series")


def handle_series(update, context):
    """Handle responses from the user when clicking menu buttons"""
    query = update.callback_query

    # Get details about the series
    show_details = get_series_by_id(query.data)

    # Create button menu
    button_list = [InlineKeyboardButton("Do it!", callback_data="vv" + query.data),
                   InlineKeyboardButton("No", callback_data="cancel")]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, 2))

    # Edit message text and ask user to choose a show
    new_text = "Is this the series you're looking for?\n\n*{}* - {}\n\n{}\n\n{}".format(show_details["Title"],
                                                                                        show_details["Year"],
                                                                                        show_details["Plot"],
                                                                                        show_details["Actors"])
    query.edit_message_text(new_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


def handle_cancel(update, context):
    """Handle button response to cancel operation"""
    query = update.callback_query
    query.edit_message_text(text="Operation cancelled!")


def handle_validate(update, context):
    """Handle the validation action by creating the series and the edge"""
    query = update.callback_query

    series_id = query.data[2:]
    show_details = get_series_by_id(series_id)

    db = Database.instance()
    # Create the series document
    # TODO Add more data
    series = db.add_series(show_details["imdbID"],
                           show_details["Title"],
                           show_details["Year"],
                           show_details["Poster"],
                           show_details["totalSeasons"])

    # Get the user document
    user_id = update.callback_query.message.chat.id
    user = db.users_col[user_id]

    # Create an edge between the documents
    db.follow_series(user, series)

    # Send success message
    text = "You are now following *{}*[.]({})".format(show_details["Title"], show_details["Poster"])
    query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN)


def handle_get_seasons(update, context):
    """Handle selection of the watched season of a show"""
    query = update.callback_query

    # Get seasons of the show
    db = Database.instance()
    seasons = db.get_seasons_by_serie_id(query.data[10:])
    series = db.get_show_by_id(query.data[10:])

    # Create button menu
    button_list = [InlineKeyboardButton("Season {}".format(season["number"]),
                                        callback_data="isWatching" + season["_key"]) for season in seasons]
    button_list.append(InlineKeyboardButton("Cancel", callback_data="cancel"))

    reply_markup = InlineKeyboardMarkup(build_menu(button_list, 2))

    # Edit message text and ask user to choose a season
    # TODO add all info in our arango DB (plot, actors, ...) and print it
    new_text = "*{}* - {}\n\nSelect the season that you watched :".format(series["title"], series["year"])
    query.edit_message_text(new_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)


def handle_is_watching(update, context):
    """Handle selection of the watched episode of a season of a show"""
    query = update.callback_query
    season_id = query.data[10:]

    # Get episodes of the season
    db = Database.instance()
    episodes = db.get_episodes_by_season_id(season_id)
    nb_episodes = len(episodes)

    # Create button menu
    button_list = [InlineKeyboardButton("Episode {}".format(episode["number"]),
                                        callback_data="logEpisode" + episode["_key"]) for episode in episodes]
    button_list.append(InlineKeyboardButton("Episode {}".format(nb_episodes + 1),
                                            callback_data="makeAndLog" + season_id + '.' + str(nb_episodes + 1)))
    button_list.append(InlineKeyboardButton("Cancel", callback_data="cancel"))

    reply_markup = InlineKeyboardMarkup(build_menu(button_list, 2))

    query.edit_message_text(text="Select the episode that you watched :", reply_markup=reply_markup)


def handle_log_episode(update, context):
    query = update.callback_query
    episode_id = query.data[10:]
    user_id = query.message.chat.id
    # Get episodes of the season
    db = Database.instance()
    db.has_seen(user_id, episode_id)

    query.edit_message_text(text="Your progress has been updated!")


def handle_create_episode(update, context):
    query = update.callback_query
    episode_id = query.data[10:]

    # Get episodes of the season
    db = Database.instance()
    db.add_episode(episode_id)

    # Link the new episode with the user (HAS_SEEN relation)
    handle_log_episode(update, context)
