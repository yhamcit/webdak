
import sqlalchemy

from sqlalchemy.exc import ArgumentError

from webapps.language.decorators.singleton import singleton
from webapps.language.errors.enverror import UnsupportedDatabase

from webapps.model.properties.dao.databaseenvironment import DatabaseEnvironment


@singleton
class DatabaseConnectorFactory(object):
    __SQLITE__ = "sqlite"

    def __init__(self) -> None:
        pass

    def create_connector(self, env: DatabaseEnvironment) -> sqlalchemy.engine:

        if env.type == DatabaseConnectorFactory.__SQLITE__:
            return self.create_sqlite_connection(env)
        else :
            raise UnsupportedDatabase("Database type: {} sepcified in environment configuration is not supported.".format(db_type))
    
    def create_sqlite_connection(self, sqlite_env: DatabaseEnvironment) -> sqlalchemy.engine:
        # TODO: verify database configuration contents
        if not sqlite_env.netloc:
            sqlite_uri = r"{}://{}".format(sqlite_env.scheme, sqlite_env.path)
        else:
            sqlite_uri = sqlite_env.uri

        try:
            en = sqlalchemy.create_engine(sqlite_uri, echo=True)
        except ArgumentError as error:
            # TODO: log
            pass
