from pony import Database

class Sqlitedbs():
    def __init__(self, in_memory: bool= False, db_store: str='', **kwargs):
        self.database = Database()

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
            self.database.bind(provider='sqlite', filename=db_store)

    def entity_cls(self, cls):
        return type(cls.__name__, (self.database.Entity, ))
    
