
from dataclasses import fields, is_dataclass, make_dataclass
from os import getcwd

from inspect import getmembers, isclass

from pony.orm import Database



db = Database()

class Sqlitedbs():
    def __init__(self, in_memory: bool= False, db_store: str='', **kwargs):
        self.database = db
        cwd = getcwd()

        if in_memory:
            THREADING = 'threading'

            if THREADING not in kwargs:
                raise ValueError(f"Database threading support must be specified when in_memory='True'")
            if kwargs[THREADING]:
                self.database.bind(provider='sqlite', filename=':sharedmemory:')
            else:
                self.database.bind(provider='sqlite', filename=':memory:')

        elif not db_store:
            raise ValueError(f"Database storage name must be provided and '{db_store}' is not valid value when in_memory='False'")

        else:
            self.database.bind(provider='sqlite', filename=f"{cwd}/{db_store}", create_db=True)

    def entity_cls(self, cls):
        return type(cls.__name__, (self.database.Entity, ))
    

    def create_table_if_not_exist(self, module):

        for name, cls in (m for m in getmembers(module) if isclass(m[1])):
            if is_dataclass(cls):
                new_cls = make_dataclass(name, 
                                         [(f.name, f.type, f.default) for f in fields(cls)], 
                                         bases=(db.Entity, ), 
                                         module=module.__name__)

                setattr(module, name, new_cls)

