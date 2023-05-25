

class EnvironmentError(Exception):
    pass

class ConfigFileError(EnvironmentError):
    pass

class ConfigContentError(EnvironmentError):
    pass

class UnsupportedDatabase(EnvironmentError):
    pass

class UnsupportedRedisMode(EnvironmentError):
    pass
