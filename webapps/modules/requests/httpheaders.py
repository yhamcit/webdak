
from typing import Iterable

from httpx import Headers

from webapps.modules.requests.dao.http_errors import HttpInvalideHeaders


class HttpHeaders(object):

    _HDR_CHARSET_               = "Accept-Charset"
    _HDV_CAHRSET_UTF8_DEFAULT_  = "utf-8, iso-8859-1; q=1"
    _HDR_CONTENT_TYPE_          = "Content-Type"
    _HDV_MIME_JSON_             = "application/json"

    _HTTP_DEFAULT_HEADERS_LIST_ = tuple((
        _HDR_CHARSET_, 
    ))

    _HTTP_DEFAULT_HEADERS_      = {_HDR_CHARSET_: _HDV_CAHRSET_UTF8_DEFAULT_}

    def __init__(self, defaults: (dict, Headers)= _HTTP_DEFAULT_HEADERS_) -> None:

        assert defaults

        if isinstance(defaults, Headers):
            self._mapset = dict(defaults.items())
        else:
            self._mapset = dict(defaults)
        
        if HttpHeaders._HDR_CHARSET_ not in defaults:
            self._mapset |= HttpHeaders._HTTP_DEFAULT_HEADERS_
    
    @property
    def mapset(self) -> dict:
        return self._mapset
    
    @mapset.setter
    def mapset(self, headers: dict):
        self._mapset = headers
    
    @property
    def char_set(self) -> str:
        return self._mapset[HttpHeaders._HDR_CHARSET_]
    
    @char_set.setter
    def char_set(self, char_set: str):
        self._mapset[HttpHeaders._HDR_CHARSET_] = char_set
    
    @property
    def content_type(self) -> str:
        return self._mapset[HttpHeaders._HDR_CONTENT_TYPE_]
    
    @content_type.setter
    def content_type(self, content_type: str):
        self._mapset[HttpHeaders._HDR_CONTENT_TYPE_] = content_type

    def update(self, headers, opt_in: tuple =None) -> None:

        if isinstance(headers, dict):
            renew_mapset = headers
        elif isinstance(headers, HttpHeaders):
            renew_mapset =  headers._mapset
        else:
            raise HttpInvalideHeaders(f"{headers}")

        mapset = self._mapset | renew_mapset

        if opt_in:
            self._mapset = dict({key: mapset[key] for key in mapset})
        else:
            self._mapset = mapset
        

    def union(self, header_maps: dict) -> dict:
        return self._mapset | header_maps
    

    def __iter__(self) -> Iterable[tuple]:
        if not self._mapset:
            raise StopIteration()

        for k, v in self._mapset.items():
            yield k, v

