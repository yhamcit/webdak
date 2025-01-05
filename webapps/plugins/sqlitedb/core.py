from typing import Generator

from webapps.language.decorators.singleton import Singleton

from webapps.model.properties.dao.plugin_class_properties import PluginClassProperties

from webapps.plugins.sqlitedb.model.properties.dbprops import SqliteProperties
from webapps.plugins.sqlitedb.sqlite import Sqlitedbs

@Singleton
class SqlitePlugin():

    def __init__(self, name: str=None, props: PluginClassProperties=None) -> None:
        super().__init__()
        self._name = name
        self._props = SqliteProperties(name, props.valueset)
        self._database = self._props.database

        self._database = Sqlitedbs(db_store=self._database.store)


