from typing import Generator

from importlib import import_module

from webapps.language.decorators.singleton import Singleton

from webapps.model.properties.dao.plugin_class_properties import PluginClassProperties

from webapps.modules.plugin.plugin import Plugin
from webapps.modules.plugin.endpoints import PluginEndpoint
from webapps.plugins.publicdebt.model.properties.debtquery import DebtQueryProfile, DebtQueryProperties
from webapps.plugins.sqlitedb.core import SqlitePlugin



@Singleton
class PublicDebtPlugin(Plugin):

    def __init__(self, name: str, props: PluginClassProperties) -> None:
        super().__init__()
        self._name = name
        self._props = DebtQueryProperties(name, props.valueset)

        self._database = SqlitePlugin(name="sqlite", props=self._props.database_profiles)
        self._database.create_table_if_not_exist()



    def endpoints(self) -> Generator[PluginEndpoint, None, None]:

        for profile in (DebtQueryProfile(valueset, self._props) for valueset in self._props.endpoint_profiles):
            ep_module = import_module(profile.package_name)
            ep_cls = getattr(ep_module, profile.class_name)
            yield ep_cls(profile.name, profile, self._props)

