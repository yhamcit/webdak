
from webapps.language.decorators.singleton import singleton

from webapps.language.errors.promiseerror import PromisePoolOccupied

from webapps.modules.asyncoroutine.promise import Promise


@singleton
class PromisePool(object):

    def __init__(self, channel_list: tuple) -> None:
        self._channels = dict(((name, dict()) for name in channel_list))

    @property
    def channels(self) :
        return self._channels

    async def the_promise(self, channel: str, name: str, identifier: str):
        channel = self.channels[channel]
        follow = Promise()
        channel[name] = follow

        try:
            promise = await follow 
        except StopAsyncIteration as done:
            # TODO: 
            pass

        if channel[name] is not None:
            raise PromisePoolOccupied(
                "There is another coroutine pending on promise({identifier}) {name} at channel {channel})" \
                    .format(channel = channel, name = name, identifier = identifier))
        
        channel[name] = promise


    def make_the_promise(self, channel: str, name: str, identifier: str):
        channel = self.channels[channel]
        promise = Promise()

        try:
            followee_promise = channel[name]
            followee_promise.send(promise)
        except StopAsyncIteration as done:
            pass
        else:
            # TODO: what exception
            raise Exception()

        return promise
