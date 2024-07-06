"""Initial space for no any utility without defined topic/submodule"""

import functools
import inspect
import typing
from datetime import date
from itertools import islice

from lseg_analytics import _feature_flags as fflags
from lseg_analytics.exceptions import (
    General404Error,
    ResourceNotFoundByServer,
    ServerException,
    UnknownServerError,
)
from lseg_analytics_basic_client.models import CalendarRelatedResource

if typing.TYPE_CHECKING:
    from lseg_analytics_basic_client.models import ServiceErrorResponse


def is_date_annotation(annotation) -> bool:
    """Is typing annotation a date, optional date, or union with date?"""
    if typing.get_origin(annotation) is typing.Union:
        return date in typing.get_args(annotation)

    return annotation == date


def parse_incoming_dates(func: typing.Callable):
    """If function or method has date annotated variables - accept also ISO date strings

    ISO strings will be converted to dates.
    Warning: Typing annotations of the processed function stays the same.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args = list(args)
        params = inspect.signature(func).parameters
        for index, (name, param) in enumerate(islice(params.items(), len(args))):
            if is_date_annotation(param.annotation) and isinstance(args[index], str):
                args[index] = date.fromisoformat(args[index])
        for name, value in kwargs.items():
            # Exclude "private" parameters
            if name.startswith("_"):
                continue
            if is_date_annotation(params[name].annotation) and isinstance(value, str):
                kwargs[name] = date.fromisoformat(value)
        return func(*args, **kwargs)

    return wrapper


def _repr_full_name(space, name, joined_prefix=False):
    return (
        ("space.name=" if joined_prefix else "") + f"'{space}.{name}'"
        if fflags.REPR_SHOW_JOINED_SPACE_NAME
        else f"space={space!r} name={name!r}"
    )


def _at_id_string(obj):
    return f" at {hex(id(obj))}"


def main_object_repr(obj):
    """Generate representation for main API object"""

    cal_id = obj.id
    name = obj.__class__.__name__

    if not hasattr(obj, "_data"):  # Can't work with object properties without it
        return f"<{name} not fully initialized>"

    full_name = _repr_full_name(obj.location.space, obj.location.name)
    _id = _at_id_string(obj) if fflags.REPR_SHOW_ID_HEX else ""
    saved_status = ""

    if fflags.REPR_SHOW_ON_SERVER_STATUS:
        saved_status = "unsaved"

        if cal_id is not None:
            saved_prefix = ""
            cal_id_str = cal_id[:8] + "‥" if fflags.REPR_SHORTEN_SERVER_ID else cal_id
            saved_status = saved_prefix + cal_id_str

        saved_status = " " + saved_status
    return f"<{name} {full_name}{saved_status}{_id}>"


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


def check_and_raise(response: "ServiceErrorResponse", logger, name: str = None, resource_id: str = None):
    """Check server response and raise exception if needed"""
    if not hasattr(response, "error"):
        return
    if getattr(response, "error", None):
        if get_error_code(response) == "404":
            if name and resource_id:  # TODO: How to make sure that they are passed where it's required?
                logger.error(f"{name} with id={resource_id} not found")
                raise ResourceNotFoundByServer(response.error)
            else:
                raise General404Error(response.error)
        raise ServerException(response.error)
    else:
        raise UnknownServerError(response)


def universal_resource_id_to_related_kwargs(inp: str):
    if "." in inp:
        # It's not resource id, it's "<space>.<name>"
        # Name can't contain have dots, but space can be multi-level later
        space, name = inp.rsplit(".", maxsplit=1)
        return {"location": {"space": space, "name": name}}
    else:
        return {"id": inp}


def convert_to_related(calendars):
    if calendars is None:
        return []
    result = []
    for calendar in calendars:
        if isinstance(calendar, str):
            rel = CalendarRelatedResource(**universal_resource_id_to_related_kwargs(calendar))
            result.append(rel)
        else:
            result.append(calendar)
    return result
