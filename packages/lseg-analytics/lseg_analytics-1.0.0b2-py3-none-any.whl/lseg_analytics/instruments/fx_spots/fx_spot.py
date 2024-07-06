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
    Description,
    FxSpotAnalyticsPricing,
    FxSpotAnalyticsValuation,
    FxSpotAsCollectionItem,
    FxSpotInstrument,
    FxSpotOnTheFlyPriceRequest,
    FxSpotOnTheFlyValuationRequest,
    FxSpotPriceRequest,
    FxSpotResource,
    FxSpotValuationRequest,
    Location,
    MarketDataInput,
    PricingParameters,
    ResourceType,
)

from ._logger import logger


class FxSpot:
    """
    FxSpot object.

    Contains all the necessary information to identify and define a FxSpot instance.

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
    definition : FxSpotInstrument
        The definition of the Fx spot instument.

    See Also
    --------
    FxSpot.price : Price a Fx Spot Instrument (pre-trade)
    FxSpot.value : Valuate a Fx Spot Instrument (post-trade)

    Examples
    --------
    Create a FxSpot instance.

    >>> fx_spot = FxSpot(FxSpotInstrument(FxRate(CrossCurrencyInput("USDEUR"))))

    Save this instance with name and space.

    >>> fx_spot.save(name = "myFxSpot", space="MySpace")
    True

    """

    _definition_class = FxSpotInstrument

    def __init__(
        self,
        definition: FxSpotInstrument,
        description: Optional[Description] = Description(tags=[]),
    ):
        """
        FxSpot constructor

        Parameters
        ----------
        definition : FxSpotInstrument
            The definition of the Fx spot instument.
        description : Description, optional
            Description object that contains the resource summary and tags.

        Examples
        --------
        Create a FxSpot instance.

        >>> fx_spot = FxSpot(FxSpotInstrument(FxRate(CrossCurrencyInput("USDEUR"))))

        """
        self.description: Optional[Description] = description
        self.definition: FxSpotInstrument = definition
        self.type: Optional[Union[str, ResourceType]] = "FxSpot"
        self._location: Location = Location(name="")
        self._id: Optional[str] = None

    @property
    def id(self):
        """
        Returns the FxSpot id

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
        Returns the FxSpot location

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
            logger.info(f"Creating FxSpotResource")

            response = check_and_raise(
                Client().fx_spots_resource.create(
                    body=FxSpotResource(
                        location=location,
                        description=self.description,
                        definition=self.definition,
                    )
                )
            )

            self._id = response.data.id

            self._location = response.data.location
            logger.info(f"FxSpotResource created with id:  {self._id}")
        except Exception as err:
            logger.error(f"Error creating FxSpotResource:  {err}")
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
        logger.info(f"Overwriting FxSpotResource with id: {self._id}")
        check_and_raise(
            Client().fx_spot_resource.overwrite(
                body=FxSpotResource(
                    location=self._location,
                    description=self.description,
                    definition=self.definition,
                ),
                instrument_id=self._id,
            )
        )

    def price(
        self,
        *,
        parameters: Optional[PricingParameters] = None,
        market_data: Optional[MarketDataInput] = None,
    ) -> FxSpotAnalyticsPricing:
        """
        Price a Fx Spot Instrument (pre-trade)

        Parameters
        ----------
        parameters : PricingParameters, optional
            Base cross asset calculation parameters.
        market_data : MarketDataInput, optional
            An object defining market data to be used to compute the analytics.

        Returns
        --------
        FxSpotAnalyticsPricing
            Object defining output of Fx Spot pricing analysis

        Examples
        --------
        Calling price on a FxSpot instance

        >>> fx_spot.price()
        {'description': {'endDate': {'adjusted': '2024-04-17', 'date': '2024-04-17', 'dateMovingConvention': 'ModifiedFollowing', 'processingInformation': 'abc', 'referenceDate': 'SpotDate', 'unAdjusted': '2024-04-17'}, 'startDate': {'adjusted': '2024-04-11', 'date': '2024-04-15', 'dateMovingConvention': 'ModifiedFollowing', 'processingInformation': 'abc', 'referenceDate': 'StartDate', 'unAdjusted': '2024-04-15'}, 'valuationDate': '2024-04-11'}, 'greeks': {'deltaAmountInDealCcy': 25644.0, 'deltaPercent': 2.04}, 'pricingAnalysis': {'dealAmount': 1072000.0, 'fxSpot': {'ask': 1.0724, 'bid': 1.072}}, 'processingInformation': ['abc']}

        Calling price on a FxSpot instance with parameters.

        >>> fx_spot.price(
        >>>         parameters=PricingParameters(
        >>>             valuation_date=datetime.date(2024, 4, 11),
        >>>             fx_pricing_preferences=FxPricingPreferences(
        >>>                 ignore_reference_currency_holidays=True,
        >>>                 reference_currency=CurrencyInput(code="USD"),
        >>>                 report_currency=CurrencyInput(code="USD"),
        >>>             )
        >>>         ),
        >>>         market_data=MarketDataInput(
        >>>             fx_forward_curves=[FxForwardCurveAsMarketDataInput(cross_currency=CrossCurrencyInput(code="USD"))]
        >>>         )
        >>>     )
        {'description': {'endDate': {'adjusted': '2024-04-17', 'date': '2024-04-17', 'dateMovingConvention': 'ModifiedFollowing', 'processingInformation': 'abc', 'referenceDate': 'SpotDate', 'unAdjusted': '2024-04-17'}, 'startDate': {'adjusted': '2024-04-11', 'date': '2024-04-15', 'dateMovingConvention': 'ModifiedFollowing', 'processingInformation': 'abc', 'referenceDate': 'StartDate', 'unAdjusted': '2024-04-15'}, 'valuationDate': '2024-04-11'}, 'greeks': {'deltaAmountInDealCcy': 25644.0, 'deltaPercent': 2.04}, 'pricingAnalysis': {'dealAmount': 1072000.0, 'fxSpot': {'ask': 1.0724, 'bid': 1.072}}, 'processingInformation': ['abc']}

        """

        try:

            response = None

            if self._id:

                response = check_and_raise(
                    Client().fx_spot_resource.price(
                        body=FxSpotPriceRequest(parameters=parameters, market_data=market_data),
                        instrument_id=self._id,
                    )
                )
            else:

                response = check_and_raise(
                    Client().fx_spots_resource.price_on_the_fly(
                        body=FxSpotOnTheFlyPriceRequest(
                            definition=self.definition,
                            parameters=parameters,
                            market_data=market_data,
                        )
                    )
                )

            output = response.data

            return output
        except Exception as err:

            raise err

    def value(
        self,
        *,
        parameters: Optional[PricingParameters] = None,
        market_data: Optional[MarketDataInput] = None,
    ) -> FxSpotAnalyticsValuation:
        """
        Valuate a Fx Spot Instrument (post-trade)

        Parameters
        ----------
        parameters : PricingParameters, optional
            Base cross asset calculation parameters.
        market_data : MarketDataInput, optional
            An object defining market data to be used to compute the analytics.

        Returns
        --------
        FxSpotAnalyticsValuation
            Object defining output of Fx Spot valuation analysis

        Examples
        --------
        Calling value on a FxSpot.

        >>> fx_spot.value()
        {'description': {'endDate': {'adjusted': '2024-04-11', 'date': '2024-04-11', 'dateMovingConvention': 'ModifiedFollowing', 'processingInformation': 'abc', 'referenceDate': 'ValuationDate', 'unAdjusted': '2024-04-11'}, 'startDate': {'adjusted': '2024-04-01', 'date': '2024-04-01', 'dateMovingConvention': 'ModifiedFollowing', 'processingInformation': 'abc', 'referenceDate': 'StartDate', 'unAdjusted': '2024-04-01'}, 'valuationDate': '2024-04-11'}, 'greeks': {'deltaAmountInDealCcy': 10000.0, 'deltaPercent': 1.0}, 'processingInformation': ['abc'], 'valuation': {'marketValueInDealCcy': 1010000.0}}

        Calling value on a FxSpot instance with parameters.

        >>> fx_spot.value(
        >>>         parameters=PricingParameters(
        >>>             valuation_date=datetime.date(2024, 4, 11),
        >>>             fx_pricing_preferences=FxPricingPreferences(
        >>>                 ignore_reference_currency_holidays=True,
        >>>                 reference_currency=CurrencyInput(code="USD"),
        >>>                 report_currency=CurrencyInput(code="USD"),
        >>>             )
        >>>         ),
        >>>         market_data=MarketDataInput(
        >>>             fx_forward_curves=[FxForwardCurveAsMarketDataInput(cross_currency=CrossCurrencyInput(code="USD"))]
        >>>         )
        >>>     )
        {'description': {'endDate': {'adjusted': '2024-04-11', 'date': '2024-04-11', 'dateMovingConvention': 'ModifiedFollowing', 'processingInformation': 'abc', 'referenceDate': 'ValuationDate', 'unAdjusted': '2024-04-11'}, 'startDate': {'adjusted': '2024-04-01', 'date': '2024-04-01', 'dateMovingConvention': 'ModifiedFollowing', 'processingInformation': 'abc', 'referenceDate': 'StartDate', 'unAdjusted': '2024-04-01'}, 'valuationDate': '2024-04-11'}, 'greeks': {'deltaAmountInDealCcy': 10000.0, 'deltaPercent': 1.0}, 'processingInformation': ['abc'], 'valuation': {'marketValueInDealCcy': 1010000.0}}

        """

        try:

            response = None

            if self._id:

                response = check_and_raise(
                    Client().fx_spot_resource.value(
                        body=FxSpotValuationRequest(parameters=parameters, market_data=market_data),
                        instrument_id=self._id,
                    )
                )
            else:

                response = check_and_raise(
                    Client().fx_spots_resource.value_on_the_fly(
                        body=FxSpotOnTheFlyValuationRequest(
                            definition=self.definition,
                            parameters=parameters,
                            market_data=market_data,
                        )
                    )
                )

            output = response.data

            return output
        except Exception as err:

            raise err

    def save(self, *, name: Optional[str] = None, space: Optional[str] = None) -> bool:
        """
        Save FxSpot instance in the platform store.

        Parameters
        ----------
        name : str, optional
            The FxSpot name. The name parameter must be specified when the object is first created. Thereafter it is optional.
        space : str, optional
            The space where the FxSpot is stored.  Space is like a namespace where resources are stored.  By default there are two spaces:
            LSEG is reserved for LSEG maintained resources, HOME is reserved for user's default space. If space is not specified, HOME will be used.

        Returns
        --------
        bool, optional
            True, if saved successfully, otherwise None


        Examples
        --------


        """
        try:
            logger.info(f"Saving FxSpot")
            if self._id:
                if (name or space) and (name != self._location.name or space != self._location.space):
                    raise Exception("When saving an existing resource, you may not change the name or space")
                else:
                    self._overwrite()
                    logger.info(f"FxSpot saved")
            elif name:
                location = Location(name=name, space=space)
                self._create(location=location)
                logger.info(f"FxSpot saved to space: {self._location.space} name: {self._location.name}")
            else:
                raise Exception("When saving for the first time, name must be defined.")
            return True
        except Exception as err:
            logger.info(f"FxSpot save failed")
            raise err

    def clone(self) -> "FxSpot":
        """
        Return the same object, without id, name and space

        Parameters
        ----------


        Returns
        --------
        FxSpot
            The cloned FxSpot object


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
