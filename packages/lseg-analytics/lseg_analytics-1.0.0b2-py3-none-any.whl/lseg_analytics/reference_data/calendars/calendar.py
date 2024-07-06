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
    CalculateDatesOutput,
    CalendarAsCollectionItem,
    CalendarDefinition,
    CalendarResource,
    ComputeDatesRequest,
    CountPeriodsOutput,
    CountPeriodsRequest,
    DateMovingConvention,
    DayCountBasis,
    Description,
    Frequency,
    GenerateDateScheduleRequest,
    GenerateHolidaysRequest,
    HolidayOutput,
    Location,
    PeriodType,
    ResourceType,
    WeekDay,
)

from ._logger import logger


class Calendar:
    """
    Calendar object.

    Contains all the necessary information to identify and define a Calendar instance.

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
    definition : CalendarDefinition
        Calendar definition object that contains rest days, first day of week, holiday rules and holiday exception rules.

    See Also
    --------
    Calendar.generateHolidays : List holidays
    Calendar.computeDates : Compute dates
    Calendar.generateDateSchedule : Generate date schedule
    Calendar.countPeriods : Count periods

    Examples
    --------
    Create a calendar instance with parameter.

    >>> my_cal_definition = CalendarDefinition(rest_days = [
    >>>                     RestDays(
    >>>                         rest_days=[WeekDay.SATURDAY, WeekDay.SUNDAY],
    >>>                         validity_period=ValidityPeriod(
    >>>                             start_date="2024-01-01",
    >>>                             end_date="2024-12-31",
    >>>                         ),
    >>>                     )
    >>>                 ],
    >>>                     first_day_of_week = WeekDay.FRIDAY,
    >>>                     holiday_rules = [
    >>>                     HolidayRule(
    >>>                         name="New Year's Day",
    >>>                         duration=FullDayDuration(full_day=1),
    >>>                         validity_period=ValidityPeriod(
    >>>                             start_date="2024-01-01",
    >>>                             end_date="2024-12-31",
    >>>                         ),
    >>>                         when=AbsolutePositionWhen(day_of_month=1, month=Month.JANUARY),
    >>>                     ),
    >>>                 ]
    >>>                 )
    >>> my_cal = Calendar(definition=my_cal_definition)

    Save this instance with name and space.

    >>> my_cal.save(name="my_calendar", space = "my_personal_space")
    True

    """

    _definition_class = CalendarDefinition

    def __init__(
        self,
        definition: CalendarDefinition,
        description: Optional[Description] = Description(tags=[]),
    ):
        """
        Calendar constructor

        Parameters
        ----------
        definition : CalendarDefinition
            Calendar definition object that contains rest days, first day of week, holiday rules and holiday exception rules.
        description : Description, optional
            Description object that contains the resource summary and tags.

        Examples
        --------
        Create a calendar instance with parameter.

        >>> my_cal_definition = CalendarDefinition(rest_days = [
        >>>                     RestDays(
        >>>                         rest_days=[WeekDay.SATURDAY, WeekDay.SUNDAY],
        >>>                         validity_period=ValidityPeriod(
        >>>                             start_date="2024-01-01",
        >>>                             end_date="2024-12-31",
        >>>                         ),
        >>>                     )
        >>>                 ],
        >>>                     first_day_of_week = WeekDay.FRIDAY,
        >>>                     holiday_rules = [
        >>>                     HolidayRule(
        >>>                         name="New Year's Day",
        >>>                         duration=FullDayDuration(full_day=1),
        >>>                         validity_period=ValidityPeriod(
        >>>                             start_date="2024-01-01",
        >>>                             end_date="2024-12-31",
        >>>                         ),
        >>>                         when=AbsolutePositionWhen(day_of_month=1, month=Month.JANUARY),
        >>>                     ),
        >>>                 ]
        >>>                 )
        >>> my_cal = Calendar(definition=my_cal_definition)

        """
        self.description: Optional[Description] = description
        self.definition: CalendarDefinition = definition
        self.type: Optional[Union[str, ResourceType]] = "Calendar"
        self._location: Location = Location(name="")
        self._id: Optional[str] = None

    @property
    def id(self):
        """
        Returns the Calendar id

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
        Returns the Calendar location

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

    def compute_dates(
        self,
        *,
        tenors: List[str],
        start_date: Optional[Union[str, datetime.date]] = None,
        date_moving_convention: Optional[Union[str, DateMovingConvention]] = None,
    ) -> List[CalculateDatesOutput]:
        """
        Compute dates

        Parameters
        ----------
        tenors : List[str]
            Tenors to be added to startDate to calculate the resulted dates (e.g., 1M, 1Y).
        start_date : Union[str, datetime.date], optional
            The start date of the calculation. The value is expressed in ISO 8601 format: YYYY-MM-DD (e.g., 2023-01-01).
        date_moving_convention : Union[str, DateMovingConvention], optional
            The method to adjust dates to working days.

        Returns
        --------
        List[CalculateDatesOutput]
            The result of the date calculation.

        Examples
        --------
        >>> my_cal.compute_dates(start_date="2023-11-01", date_moving_convention=DateMovingConvention.NEXT_BUSINESS_DAY, tenors=["1M", "2M"])
        [{'endDate': '2023-11-03', 'processingInformation': '<string>', 'tenor': '1M'},
         {'endDate': '2023-12-03', 'processingInformation': '<string>', 'tenor': '2M'}]

        """

        try:
            logger.info(f"Calling computeDates for calendarResource with id")

            response = check_and_raise(
                Client().calendar_resource.compute_dates(
                    body=ComputeDatesRequest(
                        tenors=tenors,
                        start_date=start_date,
                        date_moving_convention=date_moving_convention,
                    ),
                    calendar_id=self._id,
                )
            )

            output = response.data
            logger.info(f"Called computeDates for calendarResource with id")

            return output
        except Exception as err:
            logger.error(f"Error computeDates for calendarResource with id {err}")

            raise err

    def count_periods(
        self,
        *,
        start_date: Union[str, datetime.date],
        end_date: Union[str, datetime.date],
        day_count_basis: Optional[Union[str, DayCountBasis]] = None,
        period_type: Optional[Union[str, PeriodType]] = None,
    ) -> CountPeriodsOutput:
        """
        Count periods

        Parameters
        ----------
        start_date : Union[str, datetime.date]
            start date for counting periods
        end_date : Union[str, datetime.date]
            end date for counting periods
        day_count_basis : Union[str, DayCountBasis], optional
            The day count basis convention used to calculate the period between two dates.

            It is used when periodType is set to Year.
            Each convention defines the number of days between two dates and the year length in days (basis) for the period calculation.
        period_type : Union[str, PeriodType], optional
            The method of the period calculation.

        Returns
        --------
        CountPeriodsOutput
            The result of the period calculation.

        Examples
        --------
        >>> my_cal.count_periods(start_date="2020-01-01", end_date="2021-01-01", day_count_basis=DayCountBasis.DCB_30_360, period_type=PeriodType.DAY)
        {'count': 13.0, 'periodType': 'WorkingDay', 'processingInformation': ''}

        """

        try:
            logger.info(f"Calling countPeriods for calendarResource with id")

            response = check_and_raise(
                Client().calendar_resource.count_periods(
                    body=CountPeriodsRequest(
                        start_date=start_date,
                        end_date=end_date,
                        day_count_basis=day_count_basis,
                        period_type=period_type,
                    ),
                    calendar_id=self._id,
                )
            )

            output = response.data
            logger.info(f"Called countPeriods for calendarResource with id")

            return output
        except Exception as err:
            logger.error(f"Error countPeriods for calendarResource with id {err}")

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
            logger.info(f"Creating CalendarResource")

            response = check_and_raise(
                Client().calendars_resource.create(
                    body=CalendarResource(
                        location=location,
                        description=self.description,
                        definition=self.definition,
                    )
                )
            )

            self._id = response.data.id

            self._location = response.data.location
            logger.info(f"CalendarResource created with id:  {self._id}")
        except Exception as err:
            logger.error(f"Error creating CalendarResource:  {err}")
            raise err

    def generate_date_schedule(
        self,
        *,
        frequency: Union[str, Frequency],
        start_date: Optional[Union[str, datetime.date]] = None,
        end_date: Optional[Union[str, datetime.date]] = None,
        calendar_day_of_month: Optional[int] = None,
        count: Optional[int] = None,
        day_of_week: Optional[Union[str, WeekDay]] = None,
    ) -> List[datetime.date]:
        """
        Generate date schedule

        Parameters
        ----------
        frequency : Union[str, Frequency]
            The frequency of dates in the schedule which should be generated.
        start_date : Union[str, datetime.date], optional
            The start date of the calculation. The value is expressed in ISO 8601 format: YYYY-MM-DD (e.g., 2023-01-01).

            The start date must be less or equal to the end date.
            Required if endDate is in the past.
        end_date : Union[str, datetime.date], optional
            The end date of the calculation. The value is expressed in ISO 8601 format: YYYY-MM-DD (e.g., 2024-01-01).

            If startDate is not specified, endDate is used to define the list of dates from today's date to the end date.
            The end date must be greater or equal to the start date.
            Required if count is not specified. Only one of endDate and count can be set at a time.
        calendar_day_of_month : int, optional
            The number of the day of the month. Required if frequency is Monthly; do not use otherwise. The minimum value is 1. The maximum value is 31.
        count : int, optional
            The number is used to define a list of dates counting from the start date (or today's date if the start day is not set) to the end date.

            It should not have a negative value.
            Required if endDate is not specified. Only one of endDate and count can be set at a time.
        day_of_week : Union[str, WeekDay], optional
            The day of the week. Required if frequency is Daily; do not use otherwise.

        Returns
        --------
        List[datetime.date]
            A date on a calendar without a time zone, e.g. "April 10th"

        Examples
        --------
        >>> my_cal.generate_date_schedule(start_date='2023-05-05', end_date='2023-12-05', frequency=Frequency.WEEKLY, count=20, day_of_week=WeekDay.TUESDAY)
        [datetime.date(2023, 5, 9),
         datetime.date(2023, 5, 16),
         datetime.date(2023, 5, 23),
         datetime.date(2023, 5, 30),
         datetime.date(2023, 6, 6),
         datetime.date(2023, 6, 13),
         datetime.date(2023, 6, 20),
         datetime.date(2023, 6, 27),
         datetime.date(2023, 7, 4),
         datetime.date(2023, 7, 11),
         datetime.date(2023, 7, 18),
         datetime.date(2023, 7, 25),
         datetime.date(2023, 8, 1),
         datetime.date(2023, 8, 8),
         datetime.date(2023, 8, 15),
         datetime.date(2023, 8, 22),
         datetime.date(2023, 8, 29),
         datetime.date(2023, 9, 5),
         datetime.date(2023, 9, 12),
         datetime.date(2023, 9, 19)]

        """

        try:
            logger.info(f"Calling generateDateSchedule for calendarResource with id")

            response = check_and_raise(
                Client().calendar_resource.generate_date_schedule(
                    body=GenerateDateScheduleRequest(
                        frequency=frequency,
                        start_date=start_date,
                        end_date=end_date,
                        calendar_day_of_month=calendar_day_of_month,
                        count=count,
                        day_of_week=day_of_week,
                    ),
                    calendar_id=self._id,
                )
            )

            output = response.data
            logger.info(f"Called generateDateSchedule for calendarResource with id")

            return output
        except Exception as err:
            logger.error(f"Error generateDateSchedule for calendarResource with id {err}")

            raise err

    def generate_holidays(
        self,
        *,
        start_date: Optional[Union[str, datetime.date]] = None,
        end_date: Optional[Union[str, datetime.date]] = None,
    ) -> List[HolidayOutput]:
        """
        List holidays

        Parameters
        ----------
        start_date : Union[str, datetime.date], optional
            The start date of the calculation. The value is expressed in ISO 8601 format: YYYY-MM-DD (e.g., 2023-01-01).
        end_date : Union[str, datetime.date], optional
            The end date of the calculation. The value is expressed in ISO 8601 format: YYYY-MM-DD (e.g., 2024-01-01).

        Returns
        --------
        List[HolidayOutput]
            Dates and names of holidays for a requested calendar

        Examples
        --------
        >>> response = my_cal.generate_holidays(start_date='2023-01-01', end_date='2023-01-31')
        >>> response[0]
        {'date': '2023-01-01', 'names': [{'name': "New Year's Day", 'calendars': [{'type': 'Calendar', 'id': '125B1FCD-6EE9-4B1F-870F-5BA89EBE71AF', 'location': {'name': 'EMU', 'space': 'LSEG'}}, {'type': 'Calendar', 'id': '259B1FED-8MM3-4B1F-843F-5BA89EBE71AF', 'location': {'name': 'UKG', 'space': 'LSEG'}}], 'countries': ['', 'GBR']}], 'processingInformation': '<string>'}

        """

        try:
            logger.info(f"Calling generateHolidays for calendarResource with id")

            response = check_and_raise(
                Client().calendar_resource.generate_holidays(
                    body=GenerateHolidaysRequest(start_date=start_date, end_date=end_date),
                    calendar_id=self._id,
                )
            )

            output = response.data
            logger.info(f"Called generateHolidays for calendarResource with id")

            return output
        except Exception as err:
            logger.error(f"Error generateHolidays for calendarResource with id {err}")

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
        logger.info(f"Overwriting CalendarResource with id: {self._id}")
        check_and_raise(
            Client().calendar_resource.overwrite(
                body=CalendarResource(
                    location=self._location,
                    description=self.description,
                    definition=self.definition,
                ),
                calendar_id=self._id,
            )
        )

    def save(self, *, name: Optional[str] = None, space: Optional[str] = None) -> bool:
        """
        Save Calendar instance in the platform store.

        Parameters
        ----------
        name : str, optional
            The Calendar name. The name parameter must be specified when the object is first created. Thereafter it is optional.
        space : str, optional
            The space where the Calendar is stored.  Space is like a namespace where resources are stored.  By default there are two spaces:
            LSEG is reserved for LSEG maintained resources, HOME is reserved for user's default space. If space is not specified, HOME will be used.

        Returns
        --------
        bool, optional
            True, if saved successfully, otherwise None


        Examples
        --------


        """
        try:
            logger.info(f"Saving Calendar")
            if self._id:
                if (name or space) and (name != self._location.name or space != self._location.space):
                    raise Exception("When saving an existing resource, you may not change the name or space")
                else:
                    self._overwrite()
                    logger.info(f"Calendar saved")
            elif name:
                location = Location(name=name, space=space)
                self._create(location=location)
                logger.info(f"Calendar saved to space: {self._location.space} name: {self._location.name}")
            else:
                raise Exception("When saving for the first time, name must be defined.")
            return True
        except Exception as err:
            logger.info(f"Calendar save failed")
            raise err

    def clone(self) -> "Calendar":
        """
        Return the same object, without id, name and space

        Parameters
        ----------


        Returns
        --------
        Calendar
            The cloned Calendar object


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
