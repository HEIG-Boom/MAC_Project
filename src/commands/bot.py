#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Handles all commands directly related to the bot as 'help', 'start', commands.
"""
from telegram import ParseMode
from data.database import Database


def start(update, context):
    """Initialize conversation and creates user in DB"""
    # Store telegram user in the database
    user_id = update.message.chat.id
    username = update.message.chat.username
    db = Database.instance()
    db.add_user(user_id, username)

    update.message.reply_text(
        'Hi 👋\n\nI\'m the bot that keeps track of your viewing history.\nYou can search for a show you\'re '
        'interested in and keep track of the episodes.\nFor more info, type /help for the command list.',
    )


def help_handle(update, context):
    """Give the user a list of available commands"""
    update.message.reply_text(
        'Here is the list of possible commands\n\n'
        '*General* 🐒\n'
        '/start - Start the bot\n'
        '/help - Get info on how to use the bot\n\n'
        '*TV shows* 🎬\n'
        '/follow <term> - Search series that contain the given term\n'
        '/followed - Display the shows you follow\n'
        '/progress - See your progress in terms of episodes\n'
        '/friends - Find the users that have the most series in common with you\n',
        parse_mode=ParseMode.MARKDOWN
    )
