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
    BidAskMidSimpleValues,
    BidAskValues,
    BuildInDirectFromDepositsRequest,
    BuildInDirectFromFxForwardsRequest,
    CrossCurrencyInput,
    CrossCurrencySwapConstituent,
    CrossCurrencySwapConstituentDefinition,
    CrossCurrencySwapConstituentValues,
    CrossCurrencySwapInvalidConstituent,
    CurrencyInput,
    CurvePointRelatedInstruments,
    DepositConstituentDefinition,
    DepositConstituentFx,
    DepositConstituentValuesFx,
    DepositInvalidConstituentFx,
    Description,
    ExtrapolationMode,
    FieldValue,
    FxConstituentDefinition,
    FxForwardConstituent,
    FxForwardConstituentDefinition,
    FxForwardConstituentValues,
    FxForwardCurveAsCollectionItem,
    FxForwardCurveCalculationPreferences,
    FxForwardCurveConstituent,
    FxForwardCurveConstituentValues,
    FxForwardCurveData,
    FxForwardCurveDefinition,
    FxForwardCurveInterpolationMode,
    FxForwardCurveOutput,
    FxForwardCurvePoint,
    FxForwardCurvePricingParameters,
    FxForwardInvalidConstituent,
    FxInvalidConstituent,
    FxSpotConstituent,
    FxSpotConstituentDefinition,
    FxSpotConstituentValues,
    FxSpotInvalidConstituent,
    FxUnderlyingCurve,
    IndirectSourcesDeposits,
    IndirectSourcesSwaps,
    IrCurvePoint,
    IrCurvePointRelatedInstruments,
    IrUnderlyingCurve,
    Location,
    QuoteInput,
    QuoteInputDefinition,
    QuoteOutput,
    QuoteOutputDefinition,
    TenorType,
    UnderlyingCurves,
)

from ._logger import logger
from .fx_forward_curve import FxForwardCurve

__all__ = [
    "CrossCurrencySwapConstituent",
    "CrossCurrencySwapConstituentDefinition",
    "CrossCurrencySwapConstituentValues",
    "CrossCurrencySwapInvalidConstituent",
    "CurvePointRelatedInstruments",
    "DepositConstituentDefinition",
    "DepositConstituentFx",
    "DepositConstituentValuesFx",
    "DepositInvalidConstituentFx",
    "FxConstituentDefinition",
    "FxForwardConstituent",
    "FxForwardConstituentDefinition",
    "FxForwardConstituentValues",
    "FxForwardCurveAsCollectionItem",
    "FxForwardCurveCalculationPreferences",
    "FxForwardCurveConstituent",
    "FxForwardCurveConstituentValues",
    "FxForwardCurveData",
    "FxForwardCurveDefinition",
    "FxForwardCurveOutput",
    "FxForwardCurvePoint",
    "FxForwardCurvePricingParameters",
    "FxForwardInvalidConstituent",
    "FxInvalidConstituent",
    "FxSpotConstituent",
    "FxSpotConstituentDefinition",
    "FxSpotConstituentValues",
    "FxSpotInvalidConstituent",
    "FxUnderlyingCurve",
    "IndirectSourcesDeposits",
    "IndirectSourcesSwaps",
    "IrCurvePoint",
    "IrCurvePointRelatedInstruments",
    "IrUnderlyingCurve",
    "UnderlyingCurves",
    "create_from_deposits",
    "create_from_fx_forwards",
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
    Load a FxForwardCurve using its name and space

    Parameters
    ----------
    resource_id : str, optional
        The FxForwardCurve id.
        Required if name is not provided.
    name : str, optional
        The FxForwardCurve name.
        Required if resource_id is not provided. The name parameter must be specified when the object is first created. Thereafter it is optional.
    space : str, optional
        The space where the FxForwardCurve is stored. Space is like a namespace where resources are stored.  By default there are two spaces:
        LSEG is reserved for LSEG maintained resources, HOME is reserved for user's default space. If space is not specified, HOME will be used.

    Returns
    -------
    The FxForwardCurve instance.

    Examples
    --------
    Load by Id.

    >>> load(resource_id="125B1CUR-6EE9-4B1F-870F-5BA89EBE71CR")
    <lseg_analytics.market_data.fx_forward_curves.fx_forward_curve.FxForwardCurve at 0x7f223825f950>

    Load by name and space.

    >>> load(name="EURCHF Fx Forward Curve", space="MYCURVE")
    <lseg_analytics.market_data.fx_forward_curves.fx_forward_curve.FxForwardCurve at 0x7f223822ac90>

    """
    if not isinstance(resource_id, (str, type(None))):
        raise TypeError(f"Expected resource_id as a string, got {resource_id!r}")
    if resource_id:
        if name or space:
            warnings.warn("resource_id argument received, name & space arguments are ignored")
        return _load_by_id(resource_id)
    if not name:
        raise ValueError("Either resource_id or name argument should be provided")
    logger.info(f"Load FxForwardCurve {name} from space={space!r}")
    spaces = [space] if space else None
    result = search(names=[name], spaces=spaces)
    if not result:
        logger.error(f"FxForwardCurve {name} not found in space={space!r}")
        raise ResourceNotFound("FxForwardCurve", f"name={name} space={space}")
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
    Delete FxForwardCurve instance from the server.

    Parameters
    ----------
    resource_id : str, optional
        The FxForwardCurve resource ID.
        Required if name is not provided.
    name : str, optional
        The FxForwardCurve name.
        Required if resource_id is not provided.
    space : str, optional
        The space where the FxForwardCurve is stored. Space is like a namespace where resources are stored.  By default there are two spaces:
        LSEG is reserved for LSEG maintained resources, HOME is reserved for user's default space. If space is not specified, HOME will be used.

    Returns
    -------
    ServiceErrorResponse, optional
        Error response, if applicable, otherwise None

    Examples
    --------
    Delete by Id.

    >>> delete(resource_id = '125B1CUR-6EE9-4B1F-870F-5BA89EBE71CR')
    True

    Delete by name and space.

    >>> delete(name="EURCHF Fx Forward Curve", space="MYCURVE")
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
    logger.info(f"Delete FxForwardCurve {name} from space={space!r}")
    spaces = [space] if space else None
    result = search(names=[name], spaces=spaces)
    if not result:
        logger.error(f"FxForwardCurve {name} not found in space={space!r}")
        raise ResourceNotFound("FxForwardCurve", f"name={name} space={space}")
    elif not isinstance(result, list):
        raise LibraryException(f"Expected list of results, got {result}")
    return _delete_by_id(result[0].id)


def create_from_deposits(
    *,
    cross_currency: CrossCurrencyInput,
    reference_currency: Optional[CurrencyInput] = None,
    additional_tenor_types: Optional[List[Union[str, TenorType]]] = None,
    sources: Optional[IndirectSourcesDeposits] = None,
) -> FxForwardCurve:
    """
    Create fx forward curve using Deposit constituents - via reference currency

    Parameters
    ----------
    cross_currency : CrossCurrencyInput
        A string to define the currency pair of the curve.
    reference_currency : CurrencyInput, optional
        A string to define the reference currency for the cross-currency pair of the curve.
    additional_tenor_types : List[Union[str, TenorType]], optional
        An array of tenor types that can be used for instruments in addition to the standard tenor.
    sources : IndirectSourcesDeposits, optional
        An object that defines the sources containing the market data for the instruments used to create the curve definition.

    Returns
    --------
    FxForwardCurve
        FxForwardCurve

    Examples
    --------
    >>> create_from_deposits(
    >>>     cross_currency=CrossCurrencyInput(code="EURGBP"),
    >>>     reference_currency=CurrencyInput(code="USD"),
    >>>     sources=IndirectSourcesDeposits(
    >>>         base_fx_spot="ICAP",
    >>>         quoted_fx_spot="ICAP",
    >>>         base_deposit="ICAP",
    >>>         quoted_deposit="CRDA",
    >>>     ),
    >>>     additional_tenor_types=[TenorType.LONG, TenorType.END_OF_MONTH],
    >>> )
    <lseg_analytics.market_data.fx_forward_curves.fx_forward_curve.FxForwardCurve at 0x7f223a4f0e10>

    """

    try:
        logger.info(f"Calling createFromDeposits")

        response = check_and_raise(
            Client().fx_forward_curves_resource.create_definition_from_deposits_in_direct(
                body=BuildInDirectFromDepositsRequest(
                    cross_currency=cross_currency,
                    reference_currency=reference_currency,
                    additional_tenor_types=additional_tenor_types,
                    sources=sources,
                )
            )
        )

        output = response.data

        definition = output.definition
        logger.info(f"Called createFromDeposits")

        return FxForwardCurve(definition)
    except Exception as err:
        logger.error(f"Error createFromDeposits {err}")

        raise err


def create_from_fx_forwards(
    *,
    cross_currency: CrossCurrencyInput,
    reference_currency: Optional[CurrencyInput] = None,
    additional_tenor_types: Optional[List[Union[str, TenorType]]] = None,
    sources: Optional[IndirectSourcesSwaps] = None,
) -> FxForwardCurve:
    """
    Create fx forward curve using Fx Forward constituents - via reference currency

    Parameters
    ----------
    cross_currency : CrossCurrencyInput
        A string to define the currency pair of the curve.
    reference_currency : CurrencyInput, optional
        A string to define the reference currency for the cross-currency pair of the curve.
    additional_tenor_types : List[Union[str, TenorType]], optional
        An array of tenor types that can be used for instruments in addition to the standard tenor.
    sources : IndirectSourcesSwaps, optional
        An object that defines the sources containing the market data for the instruments used to create the curve definition.

    Returns
    --------
    FxForwardCurve
        FxForwardCurve

    Examples
    --------
    >>> create_from_fx_forwards(
    >>>     cross_currency=CrossCurrencyInput(code="EURGBP"),
    >>>     reference_currency=CurrencyInput(code="USD"),
    >>>     sources=IndirectSourcesSwaps(
    >>>         base_fx_spot="ICAP",
    >>>         base_fx_forwards="ICAP",
    >>>         quoted_fx_spot="TTKL",
    >>>         quoted_fx_forwards="TTKL",
    >>>     ),
    >>>     additional_tenor_types=[TenorType.LONG, TenorType.END_OF_MONTH],
    >>> )
    <lseg_analytics.market_data.fx_forward_curves.fx_forward_curve.FxForwardCurve at 0x7f223a4b7210>

    """

    try:
        logger.info(f"Calling createFromFxForwards")

        response = check_and_raise(
            Client().fx_forward_curves_resource.create_definition_from_fx_forwards_in_direct(
                body=BuildInDirectFromFxForwardsRequest(
                    cross_currency=cross_currency,
                    reference_currency=reference_currency,
                    additional_tenor_types=additional_tenor_types,
                    sources=sources,
                )
            )
        )

        output = response.data

        definition = output.definition
        logger.info(f"Called createFromFxForwards")

        return FxForwardCurve(definition)
    except Exception as err:
        logger.error(f"Error createFromFxForwards {err}")

        raise err


def _delete_by_id(curve_id: str) -> bool:
    """
    Delete resource

    Parameters
    ----------
    curve_id : str
        A sequence of textual characters.

    Returns
    --------
    bool


    Examples
    --------


    """

    try:
        logger.info(f"Deleting FxForwardCurveResource with id:  {curve_id}")
        check_and_raise(Client().fx_forward_curve_resource.delete(curve_id=curve_id))
        logger.info(f"Deleted FxForwardCurveResource with id:  {curve_id}")

        return True
    except Exception as err:
        logger.error(f"Error deleting FxForwardCurveResource with id:  {curve_id}")

        raise err


def _load_by_id(curve_id: str) -> FxForwardCurve:
    """
    Read resource

    Parameters
    ----------
    curve_id : str
        A sequence of textual characters.

    Returns
    --------
    FxForwardCurve


    Examples
    --------


    """

    try:
        logger.info(f"Opening FxForwardCurveResource with id:  {curve_id}")

        response = check_and_raise(Client().fx_forward_curve_resource.read(curve_id=curve_id))

        output = FxForwardCurve(response.data.definition, response.data.description)

        output._id = response.data.id

        output._location = response.data.location

        return output
    except Exception as err:
        logger.error(f"Error opening FxForwardCurveResource:  {err}")

        raise err


def search(
    *,
    item_per_page: Optional[int] = None,
    names: Optional[List[str]] = None,
    spaces: Optional[List[str]] = None,
    tags: Optional[List[str]] = None,
) -> List[FxForwardCurveAsCollectionItem]:
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
    List[FxForwardCurveAsCollectionItem]
        An object describing the basic properties of a FX forward curve.

    Examples
    --------
    Search all.

    >>> search()
    [{'type': 'FxForwardCurve', 'id': '125B1CUR-6EE9-4B1F-870F-5BA89EBE71CR', 'description': {'tags': ['EURCHF', 'EUR', 'CHF', 'FxForwardCurve'], 'summary': 'EURCHF Fx Forward Curve via USD and user surces'}, 'location': {'name': 'EURCHF Fx Forward Curve', 'space': 'MYCURVE'}}]

    Search by names and spaces.

    >>> search(names=["EURCHF Fx Forward Curve"], spaces= ["MYCURVE"])
    [{'type': 'FxForwardCurve', 'id': '125B1CUR-6EE9-4B1F-870F-5BA89EBE71CR', 'description': {'tags': ['EURCHF', 'EUR', 'CHF', 'FxForwardCurve'], 'summary': 'EURCHF Fx Forward Curve via USD and user surces'}, 'location': {'name': 'EURCHF Fx Forward Curve', 'space': 'MYCURVE'}}]

    """

    try:
        logger.info(f"Calling search")

        response = check_and_raise(
            Client().fx_forward_curves_resource.list(item_per_page=item_per_page, names=names, spaces=spaces, tags=tags)
        )

        output = response.data
        logger.info(f"Called search")

        return output
    except Exception as err:
        logger.error(f"Error search {err}")

        raise err
