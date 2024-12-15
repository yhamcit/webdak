

from typing import Self
from webapps.language.decorators.singleton import Singleton


@Singleton
class SQLiteDB():
    def __init__(self: Self, db_name: str=None):

        if db_name:
            sqlite
        pass