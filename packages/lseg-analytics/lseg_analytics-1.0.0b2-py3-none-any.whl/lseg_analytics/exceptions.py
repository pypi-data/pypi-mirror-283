"""Public exceptions."""

from lseg_analytics_basic_client.models import ServiceError, ServiceErrorResponse

__all__ = [
    "LibraryException",
    "ServerErrorBase",
    "UnknownServerError",
    "ServerException",
    "ResourceNotFound",
    "ResourceNotFoundByServer",
    "General404Error",
    "ValidationError",
]


class LibraryException(Exception):
    """Base class for all library exception, excluding azure ones"""


class ServerErrorBase(LibraryException):
    """Base class for all server-induced exceptions"""


class UnknownServerError(ServerErrorBase):
    """Unknown server error"""

    def __init__(self, response):
        self.response = response

    def __str__(self):
        return f"Unknown server error: {self.response}"


class ServerException(ServerErrorBase):  # TODO: rename to ServerError
    """Remote server exception"""

    def __init__(self, error: ServiceError):
        self.error = error

    def __str__(self):
        return f"Service Error: code={self.error.code} {self.error.message}"


class ResourceNotFound(LibraryException):
    """Resource not found using local logic"""

    def __init__(self, resource_name: str, resource_id: str):
        self.resource_name = resource_name
        self.resource_id = resource_id

    def __str__(self):
        return f"Resource {self.resource_name} not found by identifier {self.resource_id}"


class ResourceNotFoundByServer(ServerException):
    """REST 404 Resource not found"""


class General404Error(ServerException):
    """Non-resource 404"""


class ValidationError(LibraryException):
    """Local validation error"""


def check_and_raise(response):
    """Check server response and raise exception if needed"""
    if not isinstance(response, ServiceErrorResponse):
        return response
    if getattr(response, "error", None):
        if get_error_code(response).lower() == "not found":
            raise ResourceNotFoundByServer(response.error)
        raise ServerException(response.error)
    else:
        raise UnknownServerError(response)


def get_error_code(response: "ServiceErrorResponse") -> str:
    """Get error code from response

    We need this function because backend returns error code in different places at the moment
    """
    if response.error is None and isinstance(response.get("status"), int):
        return str(response["status"])
    elif response.error is None and "statusCode" in response:
        return str(response["statusCode"])
    elif response.error is not None:
        return response.error.status
    else:
        raise ValueError(f"Unexpected error response structure: {response}")
