
import sqlalchemy

from sqlalchemy.exc import ArgumentError

from webapps.language.decorators.singleton import Singleton
from webapps.model.properties.dao.env_errors import UnsupportedDatabase

from webapps.model.properties.dao.database_environment import DatabaseProfile


@Singleton
class DatabaseConnectorFactory(object):
    _SQLITE_ = "sqlite"

    def __init__(self) -> None:
        pass

    def create_connector(self, profile: DatabaseProfile) -> sqlalchemy.engine:

        if profile.type == DatabaseConnectorFactory._SQLITE_:
            return self.create_sqlite_connection(profile)
        else :
            raise UnsupportedDatabase(f"Database type: {profile.type} sepcified in environment configuration is not supported.")
    
    def create_sqlite_connection(self, sqlite_profile: DatabaseProfile) -> sqlalchemy.engine:
        # TODO: verify database configuration contents
        if not sqlite_profile.netloc:
            sqlite_uri = f"{sqlite_profile.scheme}://{sqlite_profile.path}"
        else:
            sqlite_uri = sqlite_profile.uri

        try:
            en = sqlalchemy.create_engine(sqlite_uri, echo=True)
        except ArgumentError as error:
            # TODO: log
            pass
