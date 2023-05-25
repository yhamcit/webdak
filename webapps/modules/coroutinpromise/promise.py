


from webapps.model.identifier import ModelIdentifier


from asyncio import Future, get_running_loop



class MetaPromise(type):

    def __new__(cls, name, bases, attrs):
        attrs.update({"_identifier": None})
        return super().__new__(cls, name, bases, attrs)


class Promise(Future, metaclass=MetaPromise):

    def __new__(cls, identifier: ModelIdentifier):
        # Get the current event loop.
        loop = get_running_loop()

        # Create a new Future object.
        future = loop.create_future()

        setattr(future, "_identifier", identifier)

        return future

    def __init__(self, identifier: ModelIdentifier) -> None:
        self._identifier = identifier

    @property
    def identifier(self) -> ModelIdentifier:
        return self._identifier

    @identifier.setter
    def identifier(self, identifier: ModelIdentifier) -> None:
        self._identifier = identifier
    


# class Promise(object):
#     """
#         Promise: Asynchronous Generator as communiction medium between corotinues

#         coro_A : 
#             # approch 1:
#             in_value = proms.await_with(out_value)

#             # approch 2:
#             async for value in <promise>:
#                 # do something

#             # approch 3:
#             async with <promise> as proms:
#                 in_value = proms.await_with(out_value)

#         coro_B :
#             <promise>.send(values)

#         coro_A :
#             <continues>
#     """
#     def __init__(self, corofunc: Coroutine, identifier: PromiseIdentifier, vaule: Any) -> None:
#         self._corofunc = corofunc
#         self._value = vaule
#         self._done = False
#         self._indentifier = identifier

#     def __await__(self):
#         return self
    
#     def __next__(self):
#         value = None
#         self.corofunc.send(value)
#         value = self._value
    
#     async def __anext__ (self):
#         pass

#     async def __aenter__(self):
#         await print("IO operations")

#     async def __aexit__(self, exc_type, exc, tb):
#         await print("IO operations")

#     __iter__ = __await__

#     def send(self, value):
#         pass

#     def throw(self, error):
#         pass

#     def asend(self, value):
#         pass

#     def athrow(self, error):
#         pass

#     def corofunc(self):
#         while self.done is not True:
#             yield

#     @property 
#     def done(self) -> bool:
#         return self._done

#     @done.setter
#     def done(self, done: bool):
#         self._done = done

#     @property 
#     def identifier(self) -> str:
#         return self._identifier

#     @identifier.setter
#     def identifier(self, identifier: str):
#         self._identifier = identifier

#     @property
#     def corofunc(self) -> Generator:
#         return self._corofunc
    
#     @corofunc.setter
#     def corofunc(self, corofunc: Generator):
#         self._corofunc = corofunc

#     @property
#     def value(self) -> Any:
#         value = self._value
#         self._value = None
#         return value
    
#     @value.setter
#     def value(self, value: Any):
#         self._value = value

#     def resolve(self, value):
#         try:
#             return self.corofunc.send(value)
#         except StopIteration as done:
#             # _timber
#             pass
#         else:
#             self.fullfill()

#     def fullfill(self) -> None:
#         pass