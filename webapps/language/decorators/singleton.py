from typing import Any

# from inspect import getmembers
# from inspect import isdatadescriptor

class singleton(type):

    def __init__(self, cls) -> Any:
        self._instance_vault = dict()
        self._wrapped_cls = cls

        # cls_attrs = getmembers(self._cls)
        # wapr_attrs = getmembers(self)
        # root_attrs = getmembers()
        # prnt_attrs =list(attr for cls in self._cls.__bases__ for attr in getmembers(cls))

        # attributes = list(set(list(zip(*cls_attrs))[0]) - 
        #                   set(list(zip(*wapr_attrs))[0]) - 
        #                   set(list(zip(*prnt_attrs))[0]))

        # for attr in filter(lambda attr : not isdatadescriptor(getattr(self._cls, attr)), attributes):
        #     self.__setattr__(attr, self._cls.__dict__[attr])

    def __new__(self, cls):
        creature = super().__new__(self, self.__name__, (cls,), {"__call__": singleton.__call__})
        return creature
        
    def __call__(self, *args, group_name = __module__, **kwargs) -> Any:

        if group_name not in self._instance_vault:
            self._instance_vault[group_name] = self._wrapped_cls(*args, **kwargs)

        return self._instance_vault[group_name]
