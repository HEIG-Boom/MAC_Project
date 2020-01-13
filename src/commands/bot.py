#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Handles all commands directly related to the bot as 'help', 'start', commands.
"""
import telegram


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    update.message.reply_text(
        'Hi 👋\n\nI\'m the bot that keeps track of your viewing history. You can search for a show you\'re '
        'interested in and keep track of the episodes. For more info, type /help for the command list.',
    )


def help_handle(update, context):
    update.message.reply_text(
        'Here is the list of possible commands\n\n'
        '*General* 🐒\n'
        '/start - start the bot\n'
        '/help - get info on how to use the bot\n\n'
        '*TV shows* 🎬\n'
        'Coming soon...',
        parse_mode=telegram.ParseMode.MARKDOWN
    )
