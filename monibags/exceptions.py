"""
Custom exceptions for MoniBags SDK
"""


class MoniBagsException(Exception):
    """Base exception for MoniBags SDK"""
    pass


class RateLimitError(MoniBagsException):
    """Raised when API rate limit is exceeded"""
    pass


class APIError(MoniBagsException):
    """Raised when API returns an error"""
    pass