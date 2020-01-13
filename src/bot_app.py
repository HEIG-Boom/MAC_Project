#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple Bot developed in the MAC course that allows you to manage a tv shows history.
Different actions are possible to interact with the tv shows database.
"""
import logging
import os

from telegram.ext import Updater, CommandHandler
from commands.bot import start, help_handle
from commands.tvshows import search_series

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Run the bot."""
    # Create the Updater and pass it the bot's TOKEN.
    updater = Updater(os.getenv('TELEGRAM_TOKEN'), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # On different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_handle))
    dp.add_handler(CommandHandler("list", search_series))

    # Log all errors
    dp.add_error_handler(error)

    # Start the bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


if __name__ == '__main__':
    main()
