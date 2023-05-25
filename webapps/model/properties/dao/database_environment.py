from urllib import parse as urlparser
from urllib.parse import ParseResult


from webapps.model.properties.dao.env_errors import ConfigContentError


class DatabaseEnvironment(object):

    _ADDR_URI_ = "add_uri"
    _URI_ = "uri"
    _AUTHID_ = "authid"
    _AUTHPASS_ = "authpass"

    def __init__(self, valueset: dict):
        self._valueset = valueset

    def __iter__(self) -> tuple:
        return (DatabaseProfile(**profile) for profile in self._valueset)
    
    @property
    def environment(self) -> dict:
        return self._valueset
    
    @environment.setter
    def environment(self, valueset: dict):
        # for each database section create environment for int.
        self._valueset = valueset


class DatabaseProfile(object):

    _SCHEME_ = "scheme"
    _NETLOC_ = "netloc"
    _PATH_ = "path"
    _QUERY_ = "queries"
    _PARAMS_ = "params"
    _FRAGMENT_ = "fragment"

    def __init__(self, type, name, addr_uri = "", uri = None, authid = "", authpass = "", **kwargs) -> None:
        self._authid = authid
        self._authpass = authpass
        self._type = type
        self._name = name

        if not uri:
            if not addr_uri:
                raise ConfigContentError(r"Database profile not contains any address info.")

            self._addr_uri = addr_uri
            try:
                self._parsed = urlparser.parse(addr_uri)
                return
            except Exception as error:
                # TODO : Handle exception
                raise ConfigContentError(error.args)
        
        try:
            addr_loc = DatabaseProfile.packnetloc(**uri[DatabaseProfile._NETLOC_])
            
            self._parsed = DatabaseProfile.packurlresolved(addr_loc, **uri)

            if addr_uri:
                self._addr_uri = urlparser.urljoin(addr_uri, self._parsed.geturl())
            else:
                self._addr_uri = self._parsed.geturl()

        except Exception as error:
            # TODO : Handle exception
            raise ConfigContentError(error.args)

    @property
    def identifier(self) -> str:
        return "&".join((self._type, self._name))

    @staticmethod
    def packurlresolved(addr_loc, scheme = "",path = "", params = {}, \
                        queries = {}, fragment = "", **kwargs) -> ParseResult:
        param_str = ",".join("=".join(i) for i in params.items())
        query_str = ",".join("=".join(i) for i in queries.items())
             
        try:
            return ParseResult(scheme, addr_loc, path, param_str, query_str, fragment)
        except Exception as error:
            # TODO : Handle exception
            raise ConfigContentError(error.args)
        

    @staticmethod
    def packnetloc(user = "", passwd = "", host = "", port = None):
        if user:
            if passwd:
                auth = "{}:{}".format(user, passwd)
            else:
                auth = user
        else:
            auth = ""

        if host:
            if port:
                loc = "{}:{}".format(host, port)
            else:
                loc = host
        else:
            return ""

        if auth:
            return "{}@{}".format(auth, loc)
        else:
            return loc

    @property
    def type(self) -> str:
        return self._type

    @property
    def name(self) -> str:
        return self._name

    @property
    def uri(self) -> str:
        return self._addr_uri

    @property
    def authuid(self) -> str:
        return self._parsed.username

    @property
    def scheme(self) -> str:
        return self._parsed.scheme

    @property
    def username(self) -> str:
        return self._parsed.username
    
    @property
    def password(self) -> str:
        return self._parsed.password
    
    @property
    def hostname(self) -> str:
        return self._parsed.hostname
    
    @property
    def port(self) -> str:
        return self._parsed.port
    
    @property
    def netloc(self) -> str:
        return DatabaseProfile.packnetloc(self.username, self.password, self.hostname, self.port)
    
    @property
    def path(self) -> str:
        return self._parsed.path
    
    @property
    def params(self) -> str:
        return self._parsed.params
    
    @property
    def query(self) -> str:
        return self._parsed.query
