
class Singleton():

    _singleton_vault = dict()

    def __new__(cls, _cls):
        _decorated_cls = type(f"{_cls.__name__}_decorated", (_cls, ), {"__new__": Singleton.__create_or_pick__})
        return _decorated_cls

    def __create_or_pick__(cls, *args, **kwds):
        if not cls.__base__ in Singleton._singleton_vault:
            singleton = object.__new__(cls.__base__)
            singleton.__init__(*args, **kwds)
            Singleton._singleton_vault[cls.__base__] = singleton

        return Singleton._singleton_vault[cls.__base__]
