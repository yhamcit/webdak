from typing import Generator

from webapps.language.decorators.singleton import Singleton

from webapps.model.properties.dao.plugin_class_properties import PluginClassProperties

from webapps.plugins.sqlitedb.model.properties.dbprops import SqliteProperties
from webapps.plugins.sqlitedb.sqlite import Sqlitedbs

@Singleton
class SqlitePlugin():

    def __init__(self, name: str=None, props: PluginClassProperties=None) -> None:
        
        self.name = name
        # self.__dict__.update(props)

        self._props = SqliteProperties(props)

        self._database = Sqlitedbs(db_store=self._props.store)

    

    def create_table_if_not_exist(self, module):
        self._database.create_table_if_not_exist(module=module)


    def generate_tables(self):
        self._database.generate_tables()

    