



from webapps.modules.coroutinpromise.promisepool import PromisePool


def require_promise(channel: str, name: str, id: str):



    def decorator(func: function) -> function:

        promise = PromisePool.require_promise(func(), channel, name, id)

        async def decroration(*args, **kwargs) :

            await PromisePool.wait_deliver(func(*args, **kwargs))
        
        return decroration
    
    return decorator