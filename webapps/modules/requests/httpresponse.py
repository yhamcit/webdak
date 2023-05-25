
from typing import Iterator
from typing import Any

from io import BytesIO
from httpx import Response

from abc import abstractmethod


class HttpResponseParser(object):

    @abstractmethod
    def deserialize(self) -> dict():
        ...

    @abstractmethod
    def serialize(self) -> str:
        ...

    @abstractmethod
    def headers(self) -> dict:
        ...

    @abstractmethod
    def streaming(self, response) -> Iterator[Response]:
        ...


class HttpDefaultJsonParser(HttpResponseParser):

    def __init__(self) -> None:
        pass

    def deserialize(self, response) -> Any:
        return response.json()

    def serialize(self, response) -> str:
        return response.text
    
    def get_url(self, response) -> str:
        return response.url
    
    def get_encoding(self, response):
        return response.encoding
    
    def streaming(self, response) -> Iterator[Response]:
        return BytesIO(response.content)
    
    def headers(self, response) -> dict:
        return response.headers