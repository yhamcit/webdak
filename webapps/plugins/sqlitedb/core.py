from asyncio import to_thread
import asyncio

from pathlib import Path
from sqlite3 import connect as connect_sqlite

from webapps.language.decorators.singleton import Singleton
from webapps.plugins.sqlitedb.model.properties.dbprops import SqliteProperties

from webapps.plugins.publicdebt.model.dao.tables import LocalPublicDebt, generat_table_stmt, insert_record_stmt, simple_query_stmt, default_query_conditions


@Singleton
class SqlitePlugin():
    def __init__(self, name: str=None, props: dict=None):

        self._props = SqliteProperties(props)

        self.db = Path(self._props.store).absolute()

        # if self._props.in_memory:

        #     assert hasattr(self._props, 'threading'), f"Database threading support must be specified when in_memory='True'"

        #     if self._props.threading:
        #         self.db.bind(provider='sqlite', filename=':sharedmemory:')
        #     else:
        #         self.db.bind(provider='sqlite', filename=':memory:')
        # else:

        #     assert hasattr(self._props, 'store'), f"Database storage name must be providedwhen in_memory='False'"
        #     assert self._props.store, f"Database storage name can not be empty, now it's : '{self._props.store}'"

            
        #     self.db.bind(provider='sqlite', filename=store_path.absolute().as_posix(), create_db=True)



    def entity_cls(self, cls):
        return type(cls.__name__, (self.db.Entity, ))
    

    def create_table_if_not_exist(self):
        asyncio.run(to_thread(run_sqlite, self.db, generat_table_stmt()))


    async def query_debt(self, params: dict=default_query_conditions):

        result = await to_thread(run_sqlite, self.db, simple_query_stmt(params))
        return result
    
    

def run_sqlite(db_uri, sql_stat, counts: int=50):

    with connect_sqlite(db_uri) as db_conn:
        sql = db_conn.cursor()
        result = sql.execute(sql_stat)

        return result.fetchmany(counts)