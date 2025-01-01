from typing import Generator

from webapps.language.decorators.singleton import Singleton

from webapps.model.properties.dao.plugin_class_properties import PluginClassProperties

from webapps.modules.plugin.plugin import Plugin
from webapps.modules.plugin.endpoints import PluginEndpoint
from webapps.plugins.publicdebt.model.dao import tables
from webapps.plugins.sqlitedb.model.properties.dbprops import SqliteProperties
from webapps.plugins.sqlitedb.sqlite import Sqlitedbs

@Singleton
class SqlitePlugin(Plugin):

    def __init__(self, name: str, props: PluginClassProperties) -> None:
        super().__init__()
        self._name = name
        self._props = SqliteProperties(name, props.valueset)
        self._database = self._props.database


        self._database = Sqlitedbs(db_store=self._database.store)
        self._database.create_table_if_not_exist(tables)


    def endpoints(self) -> Generator[PluginEndpoint, None, None]:
        for ep in ():
            yield ep
        return
