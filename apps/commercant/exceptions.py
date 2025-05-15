class InsufficientStockError(Exception):
    """Raised when product stock is insufficient"""

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class InactiveProductError(Exception):
    """Raised for operations on inactive products"""

    pass
