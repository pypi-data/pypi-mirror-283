from _typeshed import Incomplete
from odoorpc.rpc import error as error, jsonrpclib as jsonrpclib

class Connector:
    host: Incomplete
    port: Incomplete
    version: Incomplete
    def __init__(self, host, port: int = 8069, timeout: int = 120, version: Incomplete | None = None) -> None: ...
    @property
    def ssl(self): ...
    @property
    def timeout(self): ...
    @timeout.setter
    def timeout(self, timeout) -> None: ...

class ConnectorJSONRPC(Connector):
    deserialize: Incomplete
    def __init__(
        self,
        host,
        port: int = 8069,
        timeout: int = 120,
        version: Incomplete | None = None,
        deserialize: bool = True,
        opener: Incomplete | None = None,
    ) -> None: ...
    @property
    def proxy_json(self): ...
    @property
    def proxy_http(self): ...
    @property
    def timeout(self): ...
    @timeout.setter
    def timeout(self, timeout) -> None: ...

class ConnectorJSONRPCSSL(ConnectorJSONRPC):
    def __init__(
        self,
        host,
        port: int = 8069,
        timeout: int = 120,
        version: Incomplete | None = None,
        deserialize: bool = True,
        opener: Incomplete | None = None,
    ) -> None: ...
    @property
    def ssl(self): ...

PROTOCOLS: Incomplete
