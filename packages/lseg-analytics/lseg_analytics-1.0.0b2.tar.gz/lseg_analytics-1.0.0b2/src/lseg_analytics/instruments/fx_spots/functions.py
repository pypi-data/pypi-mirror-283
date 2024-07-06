import copy
import datetime
import warnings
from typing import Any, Dict, List, Optional, Union

from lseg_analytics._utils.client import Client
from lseg_analytics.common._utils import convert_to_related
from lseg_analytics.exceptions import (
    LibraryException,
    ResourceNotFound,
    check_and_raise,
)
from lseg_analytics_basic_client.models import (
    AdjustedDate,
    BidAskSimpleValues,
    CrossCurrencyInput,
    CrossCurrencySwapConstituent,
    CrossCurrencySwapConstituentDefinition,
    CurrencyInput,
    DateMovingConvention,
    DepositConstituentDefinition,
    DepositConstituentFx,
    Description,
    FxAnalyticsDescription,
    FxConstituentDefinition,
    FxForwardConstituent,
    FxForwardConstituentDefinition,
    FxForwardCurveAsMarketDataInput,
    FxForwardCurveConstituent,
    FxForwardCurveDefinition,
    FxForwardCurveRelatedResource,
    FxPayment,
    FxPricingAnalysis,
    FxPricingPreferences,
    FxRate,
    FxRisk,
    FxSpotAnalyticsDescription,
    FxSpotAnalyticsPricing,
    FxSpotAnalyticsValuation,
    FxSpotAsCollectionItem,
    FxSpotConstituent,
    FxSpotConstituentDefinition,
    FxSpotDefinition,
    FxSpotInstrument,
    FxSpotPricingAnalysis,
    FxSpotRisk,
    FxSpotValuation,
    FxValuation,
    Location,
    MarketDataInput,
    PricingParameters,
    QuoteInput,
    QuoteInputDefinition,
    ReferenceDate,
)

from ._logger import logger
from .fx_spot import FxSpot

__all__ = [
    "CrossCurrencySwapConstituent",
    "CrossCurrencySwapConstituentDefinition",
    "DepositConstituentDefinition",
    "DepositConstituentFx",
    "FxAnalyticsDescription",
    "FxConstituentDefinition",
    "FxForwardConstituent",
    "FxForwardConstituentDefinition",
    "FxForwardCurveAsMarketDataInput",
    "FxForwardCurveConstituent",
    "FxForwardCurveDefinition",
    "FxForwardCurveRelatedResource",
    "FxPayment",
    "FxPricingAnalysis",
    "FxPricingPreferences",
    "FxRate",
    "FxRisk",
    "FxSpotAnalyticsDescription",
    "FxSpotAnalyticsPricing",
    "FxSpotAnalyticsValuation",
    "FxSpotAsCollectionItem",
    "FxSpotConstituent",
    "FxSpotConstituentDefinition",
    "FxSpotDefinition",
    "FxSpotInstrument",
    "FxSpotPricingAnalysis",
    "FxSpotRisk",
    "FxSpotValuation",
    "FxValuation",
    "MarketDataInput",
    "PricingParameters",
    "delete",
    "load",
    "search",
]


@logger.hold_log_id
def load(
    *,
    resource_id: Optional[str] = None,
    name: Optional[str] = None,
    space: Optional[str] = None,
):
    """
    Load a FxSpot using its name and space

    Parameters
    ----------
    resource_id : str, optional
        The FxSpot id.
        Required if name is not provided.
    name : str, optional
        The FxSpot name.
        Required if resource_id is not provided. The name parameter must be specified when the object is first created. Thereafter it is optional.
    space : str, optional
        The space where the FxSpot is stored. Space is like a namespace where resources are stored.  By default there are two spaces:
        LSEG is reserved for LSEG maintained resources, HOME is reserved for user's default space. If space is not specified, HOME will be used.

    Returns
    -------
    The FxSpot instance.

    Examples
    --------
    Load by Id.

    >>> load(resource_id="94da9f98-343f-4dca-9b34-479987060f91")
    <lseg_analytics.instruments.fx_spots.fx_spot.FxSpot at 0x7f8e5662e7d0>

    Load by name and space.

    >>> load(name = "myFxSpot", space="MySpace")
    <lseg_analytics.instruments.fx_spots.fx_spot.FxSpot at 0x7f8e5415f090>

    """
    if not isinstance(resource_id, (str, type(None))):
        raise TypeError(f"Expected resource_id as a string, got {resource_id!r}")
    if resource_id:
        if name or space:
            warnings.warn("resource_id argument received, name & space arguments are ignored")
        return _load_by_id(resource_id)
    if not name:
        raise ValueError("Either resource_id or name argument should be provided")
    logger.info(f"Load FxSpot {name} from space={space!r}")
    spaces = [space] if space else None
    result = search(names=[name], spaces=spaces)
    if not result:
        logger.error(f"FxSpot {name} not found in space={space!r}")
        raise ResourceNotFound("FxSpot", f"name={name} space={space}")
    elif not isinstance(result, list):
        raise LibraryException(f"Expected list of results, got {result}")
    elif len(result) > 1:
        warnings.warn(f"Found more than one result for name={name!r} and space={space!r}, returning the first one")
    return _load_by_id(result[0].id)


@logger.hold_log_id
def delete(
    *,
    resource_id: Optional[str] = None,
    name: Optional[str] = None,
    space: Optional[str] = None,
):
    """
    Delete FxSpot instance from the server.

    Parameters
    ----------
    resource_id : str, optional
        The FxSpot resource ID.
        Required if name is not provided.
    name : str, optional
        The FxSpot name.
        Required if resource_id is not provided.
    space : str, optional
        The space where the FxSpot is stored. Space is like a namespace where resources are stored.  By default there are two spaces:
        LSEG is reserved for LSEG maintained resources, HOME is reserved for user's default space. If space is not specified, HOME will be used.

    Returns
    -------
    ServiceErrorResponse, optional
        Error response, if applicable, otherwise None

    Examples
    --------
    Delete by Id.

    >>> delete(resource_id="5125e2a4-f7db-48dd-ab35-7d05d6886be8")
    True

    Delete by name and space.

    >>> delete(name = "myFxSpot", space="MySpace")
    True

    """
    if not isinstance(resource_id, (str, type(None))):
        raise TypeError(f"Expected resource_id as a string, got {resource_id!r}")
    if resource_id:
        if name or space:
            warnings.warn("resource_id argument received, name & space arguments are ignored")
        return _delete_by_id(resource_id)
    if not name:
        raise ValueError("Either resource_id or name argument should be provided")
    logger.info(f"Delete FxSpot {name} from space={space!r}")
    spaces = [space] if space else None
    result = search(names=[name], spaces=spaces)
    if not result:
        logger.error(f"FxSpot {name} not found in space={space!r}")
        raise ResourceNotFound("FxSpot", f"name={name} space={space}")
    elif not isinstance(result, list):
        raise LibraryException(f"Expected list of results, got {result}")
    return _delete_by_id(result[0].id)


def _delete_by_id(instrument_id: str) -> bool:
    """
    Delete resource

    Parameters
    ----------
    instrument_id : str
        A sequence of textual characters.

    Returns
    --------
    bool


    Examples
    --------


    """

    try:
        logger.info(f"Deleting FxSpotResource with id:  {instrument_id}")
        check_and_raise(Client().fx_spot_resource.delete(instrument_id=instrument_id))
        logger.info(f"Deleted FxSpotResource with id:  {instrument_id}")

        return True
    except Exception as err:
        logger.error(f"Error deleting FxSpotResource with id:  {instrument_id}")

        raise err


def _load_by_id(instrument_id: str) -> FxSpot:
    """
    Read resource

    Parameters
    ----------
    instrument_id : str
        A sequence of textual characters.

    Returns
    --------
    FxSpot


    Examples
    --------


    """

    try:
        logger.info(f"Opening FxSpotResource with id:  {instrument_id}")

        response = check_and_raise(Client().fx_spot_resource.read(instrument_id=instrument_id))

        output = FxSpot(response.data.definition, response.data.description)

        output._id = response.data.id

        output._location = response.data.location

        return output
    except Exception as err:
        logger.error(f"Error opening FxSpotResource:  {err}")

        raise err


def search(
    *,
    item_per_page: Optional[int] = None,
    names: Optional[List[str]] = None,
    spaces: Optional[List[str]] = None,
    tags: Optional[List[str]] = None,
) -> List[FxSpotAsCollectionItem]:
    """
    List resource

    Parameters
    ----------
    item_per_page : int, optional
        A 32-bit integer. (`-2,147,483,648` to `2,147,483,647`)
    names : List[str], optional

    spaces : List[str], optional

    tags : List[str], optional


    Returns
    --------
    List[FxSpotAsCollectionItem]
        An object describing the basic properties of an FX spot.

    Examples
    --------
    Search all.

    >>> search()
    [{'type': 'FxSpot', 'id': '94da9f98-343f-4dca-9b34-479987060f91', 'location': {'name': 'Test_ToDelete', 'space': 'test'}}]

    Search by names and spaces.

    >>> search(names=["Test_ToDelete"], spaces=["test"])
    [{'type': 'FxSpot', 'id': '94da9f98-343f-4dca-9b34-479987060f91', 'location': {'name': 'Test_ToDelete', 'space': 'test'}}]

    """

    try:
        logger.info(f"Calling search")

        response = check_and_raise(
            Client().fx_spots_resource.list(item_per_page=item_per_page, names=names, spaces=spaces, tags=tags)
        )

        output = response.data
        logger.info(f"Called search")

        return output
    except Exception as err:
        logger.error(f"Error search {err}")

        raise err
