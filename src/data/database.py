from pyArango.connection import *
from pyArango.theExceptions import DocumentNotFoundError

from decorators.singleton import Singleton


@Singleton
class Database(object):
    def __init__(self):
        """Initializes the data connection"""
        database_name = "teleshows"

        conn = Connection()
        if not conn.hasDatabase(database_name):
            self.db = conn.createDatabase(name=database_name)
            self.db = conn[database_name]
            self.db.createCollection(name="Users")
        else:
            self.db = conn[database_name]

    def add_user(self, telegram_id, telegram_username):
        """Add the telegram user in the database"""
        users_collection = self.db["Users"]

        # Check if the user is already in the database
        try:
            user = users_collection[str(telegram_id)]
            # Check if the username has changed
            if user["username"] != telegram_username:
                user["username"] = telegram_username
                user.save()
        except DocumentNotFoundError:
            # Create the new user
            user = users_collection.createDocument()
            user["username"] = telegram_username
            user._key = str(telegram_id)
            user.save()

    def __str__(self):
        return 'Database connection object'
