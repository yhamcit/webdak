
from .dao.databaseenvironment import DatabaseEnvironment

from webapps.language.decorators.singleton import singleton


@singleton
class Preference(object):
    pass
