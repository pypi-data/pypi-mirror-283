from _typeshed import Incomplete

class ConnectorError(BaseException):
    message: Incomplete
    odoo_traceback: Incomplete
    def __init__(self, message, odoo_traceback: Incomplete | None = None) -> None: ...
