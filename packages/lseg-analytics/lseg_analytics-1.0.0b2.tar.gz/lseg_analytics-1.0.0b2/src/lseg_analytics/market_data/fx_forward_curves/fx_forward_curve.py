import copy
import datetime
import warnings
from typing import Any, Dict, List, Optional, Union

from lseg_analytics._utils.client import Client
from lseg_analytics.exceptions import (
    LibraryException,
    ResourceNotFound,
    check_and_raise,
)
from lseg_analytics_basic_client.models import (
    CrossCurrencyInput,
    CurrencyInput,
    Description,
    FxForwardCurveAsCollectionItem,
    FxForwardCurveCalculateOnTheFlyRequest,
    FxForwardCurveCalculateRequest,
    FxForwardCurveData,
    FxForwardCurveDefinition,
    FxForwardCurvePricingParameters,
    FxForwardCurveResource,
    IndirectSourcesDeposits,
    IndirectSourcesSwaps,
    Location,
    ResourceType,
    TenorType,
)

from ._logger import logger


class FxForwardCurve:
    """
    FxForwardCurve object.

    Contains all the necessary information to identify and define a FxForwardCurve instance.

    Attributes
    ----------
    type : Union[str, ResourceType], optional
        The resource type. Possible values are: Calendar, Currency, CrossCurrency, IrCurve, FxForwardCurve, Analytics, Loan, FxSpot, NonDeliverableForward, Deposit, CrossCurrencySwap or Space.
    id : str, optional
        Unique resource ID specified by LSEG.
    location : Location
        Location of the platform where resource is stored.
    description : Description, optional
        Description object that contains the resource summary and tags.
    definition : FxForwardCurveDefinition
        An object to define the Fx Forward Curve resource.

    See Also
    --------
    FxForwardCurve.calculate : Calculate fx forward curve points from curve definition

    Examples
    --------
    Create a FxForwardCurve instance.

    >>> fx_curve = FxForwardCurve(
    >>>     FxForwardCurveDefinition(
    >>>         cross_currency=CrossCurrencyInput(code="USDJPY"), reference_currency=CurrencyInput(code="JPY")
    >>>     )
    >>> )

    Save this instance with name and space.

    >>> fx_curve.save(name="EURCHF Fx Forward Curve", space="MYCURVE")
    True

    """

    _definition_class = FxForwardCurveDefinition

    def __init__(
        self,
        definition: FxForwardCurveDefinition,
        description: Optional[Description] = Description(tags=[]),
    ):
        """
        FxForwardCurve constructor

        Parameters
        ----------
        definition : FxForwardCurveDefinition
            An object to define the Fx Forward Curve resource.
        description : Description, optional
            Description object that contains the resource summary and tags.

        Examples
        --------
        Create a FxForwardCurve instance.

        >>> fx_curve = FxForwardCurve(
        >>>     FxForwardCurveDefinition(
        >>>         cross_currency=CrossCurrencyInput(code="USDJPY"), reference_currency=CurrencyInput(code="JPY")
        >>>     )
        >>> )

        """
        self.description: Optional[Description] = description
        self.definition: FxForwardCurveDefinition = definition
        self.type: Optional[Union[str, ResourceType]] = "FxForwardCurve"
        self._location: Location = Location(name="")
        self._id: Optional[str] = None

    @property
    def id(self):
        """
        Returns the FxForwardCurve id

        Parameters
        ----------


        Returns
        --------
        str
            Unique resource ID specified by LSEG.

        Examples
        --------


        """
        return self._id

    @id.setter
    def id(self, value):
        raise AttributeError("id is read only")

    @property
    def location(self):
        """
        Returns the FxForwardCurve location

        Parameters
        ----------


        Returns
        --------
        Location
            Location of the platform where resource is stored.

        Examples
        --------


        """
        return self._location

    @location.setter
    def location(self, value):
        raise AttributeError("location is read only")

    def calculate(self, *, parameters: Optional[FxForwardCurvePricingParameters] = None) -> FxForwardCurveData:
        """
        Calculate fx forward curve points from curve definition

        Parameters
        ----------
        parameters : FxForwardCurvePricingParameters, optional
            An object that contains parameters used to define how the Fx Forward curve is constructed from the constituents.

        Returns
        --------
        FxForwardCurveData
            An object that describes the constructed curve.

        Examples
        --------
        Calling calculate on a FxForwardCurve instance.

        >>> response = fx_curve.calculate()
        >>> response["curve"]["constituents"][0]
        {'definition': {'crossCurrency': {'code': 'EURUSD'}, 'tenor': 'SPOT'}, 'quote': {'endDate': '2022-10-14', 'startDate': '2022-10-12', 'definition': {'instrumentCode': 'EUR='}, 'values': {'ask': {'value': 0.9708}, 'bid': {'value': 0.9704}}}, 'type': <FxForwardCurveConstituentType.FX_SPOT: 'FxSpot'>}

        Calling calculate on a FxForwardCurve instance with parameters.

        >>> response = fx_curve.calculate(parameters = FxForwardCurvePricingParameters(valuation_date=datetime.date(2024, 1, 1)))
        >>> response["curve"]["constituents"][0]
        {'definition': {'crossCurrency': {'code': 'EURUSD'}, 'tenor': 'SPOT'}, 'quote': {'endDate': '2022-10-14', 'startDate': '2022-10-12', 'definition': {'instrumentCode': 'EUR='}, 'values': {'ask': {'value': 0.9708}, 'bid': {'value': 0.9704}}}, 'type': <FxForwardCurveConstituentType.FX_SPOT: 'FxSpot'>}

        """

        try:

            response = None

            if self._id:

                response = check_and_raise(
                    Client().fx_forward_curve_resource.calculate(
                        body=FxForwardCurveCalculateRequest(parameters=parameters),
                        curve_id=self._id,
                    )
                )
            else:

                response = check_and_raise(
                    Client().fx_forward_curves_resource.calculate_on_the_fly(
                        body=FxForwardCurveCalculateOnTheFlyRequest(definition=self.definition, parameters=parameters)
                    )
                )

            output = response.data

            return output
        except Exception as err:

            raise err

    def _create(self, location: Location) -> None:
        """
        Create resource

        Parameters
        ----------
        location : Location
            Location of the platform where resource is stored.

        Returns
        --------
        None


        Examples
        --------


        """

        try:
            logger.info(f"Creating FxForwardCurveResource")

            response = check_and_raise(
                Client().fx_forward_curves_resource.create(
                    body=FxForwardCurveResource(
                        location=location,
                        description=self.description,
                        definition=self.definition,
                    )
                )
            )

            self._id = response.data.id

            self._location = response.data.location
            logger.info(f"FxForwardCurveResource created with id:  {self._id}")
        except Exception as err:
            logger.error(f"Error creating FxForwardCurveResource:  {err}")
            raise err

    def _overwrite(self) -> None:
        """
        Overwrite resource

        Parameters
        ----------


        Returns
        --------
        None


        Examples
        --------


        """
        logger.info(f"Overwriting FxForwardCurveResource with id: {self._id}")
        check_and_raise(
            Client().fx_forward_curve_resource.overwrite(
                body=FxForwardCurveResource(
                    location=self._location,
                    description=self.description,
                    definition=self.definition,
                ),
                curve_id=self._id,
            )
        )

    def save(self, *, name: Optional[str] = None, space: Optional[str] = None) -> bool:
        """
        Save FxForwardCurve instance in the platform store.

        Parameters
        ----------
        name : str, optional
            The FxForwardCurve name. The name parameter must be specified when the object is first created. Thereafter it is optional.
        space : str, optional
            The space where the FxForwardCurve is stored.  Space is like a namespace where resources are stored.  By default there are two spaces:
            LSEG is reserved for LSEG maintained resources, HOME is reserved for user's default space. If space is not specified, HOME will be used.

        Returns
        --------
        bool, optional
            True, if saved successfully, otherwise None


        Examples
        --------


        """
        try:
            logger.info(f"Saving FxForwardCurve")
            if self._id:
                if (name or space) and (name != self._location.name or space != self._location.space):
                    raise Exception("When saving an existing resource, you may not change the name or space")
                else:
                    self._overwrite()
                    logger.info(f"FxForwardCurve saved")
            elif name:
                location = Location(name=name, space=space)
                self._create(location=location)
                logger.info(f"FxForwardCurve saved to space: {self._location.space} name: {self._location.name}")
            else:
                raise Exception("When saving for the first time, name must be defined.")
            return True
        except Exception as err:
            logger.info(f"FxForwardCurve save failed")
            raise err

    def clone(self) -> "FxForwardCurve":
        """
        Return the same object, without id, name and space

        Parameters
        ----------


        Returns
        --------
        FxForwardCurve
            The cloned FxForwardCurve object


        Examples
        --------


        """
        definition = self._definition_class()
        definition._data = copy.deepcopy(self.definition._data)
        description = None
        if self.description:
            description = Description()
            description._data = copy.deepcopy(self.description._data)
        return self.__class__(definition=definition, description=description)
