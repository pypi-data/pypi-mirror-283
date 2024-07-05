from functools import wraps
from os import getenv

from dotenv import load_dotenv


__all__ = ["create", "provides"]

DEFAULT_DOTENV_PATH = ".env"

_APP = None
_REGISTRY = dict()
_CACHE = dict()


class DotEnvConfig:
    """
    Default configuration provider. Uses dotenv which allows for configuration via
    environment variables and/or .env files.
    
    """
    def __init__(self, path=DEFAULT_DOTENV_PATH):
        load_dotenv(path)

    def __getattr__(self, name):
        return getenv(name.upper())


class Application:
    """
    High-level application object provides access to the dependency graph and metadata.
    
    """
    def __init__(self, identifier, config=None):
        global _CACHE, _REGISTRY

        if config is None:
            config = DotEnvConfig()

        self.identifier = identifier
        self.registry = _REGISTRY
        self.cache = _CACHE
        self.config = config

    def __getattr__(self, name):
        if name in self.cache:
            return self.cache[name]
        elif name in self.registry:
            self.cache[name] = self.registry[name](self)
            return self.cache[name]
        else:
            raise AttributeError(f"{name} is not a registered component.")
    
    def load(self, *identifiers):
        for identifier in identifiers:
            getattr(self, identifier)
        
        return self



def create(identifier: str, force: bool = True):
    """Create an application namespace associated with given identifier."""
    global _APP
    if _APP is not None and force is False:
        raise KeyError(f"Application object already initialized.")

    _APP = Application(identifier)
    _REGISTRY = dict()
    _CACHE = dict()

    return _APP   


def provides(identifier: str):
    """
    Register a dependency in the global app registry associated with given identifier.
    
    """
    global _REGISTRY

    if identifier in _REGISTRY:
        raise KeyError(f"identifier {identifier} is already assigned an object in the application.")
    
    def decorated(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        _REGISTRY[identifier] = wrapper
    
        return wrapper
        
    return decorated