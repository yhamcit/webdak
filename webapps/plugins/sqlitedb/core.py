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


    async def query_debt(self, in_key: str=None, in_cons: set=None):

        query_fields = {
            "district": None,
            "local_debt_balances": None,
            "total_debt_upper_limit": None,
            "total_local_bonds": None,
            "total_debt_amount": None,
            "total_gdp_amount": None,
            "debt_to_gdp_ratio": None,
            "local_general_public_revenue": None,
            "debt_to_revenue_ratio": None,
        }

        result = await to_thread(run_sqlite, self.db, simple_query_stmt(fields=query_fields, in_key=in_key, in_cons=in_cons))
        return result
    
    

def run_sqlite(db_uri, sql_stat, counts: int=50):

    with connect_sqlite(db_uri) as db_conn:
        sql = db_conn.cursor()
        try:
            result = sql.execute(sql_stat)
        except Exception as e:
            print(e.args)

    return result.fetchmany(counts)