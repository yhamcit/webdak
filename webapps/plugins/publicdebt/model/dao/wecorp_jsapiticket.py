
from time import time as timestamp


class CorpWechatJSApiTicket():

    def __init__(self, from_json: dict=None):

        if from_json:
            self.__dict__.update(from_json)
            self._expire_timestamp = int(timestamp()) + self.expires_in


    def is_expired(self):

        ts = int(timestamp())

        if ts + 10 >= self._expire_timestamp:
            return True
        else:
            return False
        