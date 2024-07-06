from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class MovementsBetweenStages(BaseModel):
    """Movements between stages

    :param count: The count of the deals that have been moved between stages, defaults to None
    :type count: int, optional
    """

    def __init__(self, count: int = None):
        if count is not None:
            self.count = count


@JsonMap({"currency_id": "CURRENCY_ID"})
class NewDealsValues(BaseModel):
    """The values of the deals

    :param currency_id: The value of the deals, defaults to None
    :type currency_id: int, optional
    """

    def __init__(self, currency_id: int = None):
        if currency_id is not None:
            self.currency_id = currency_id


@JsonMap({"currency_id": "CURRENCY_ID"})
class NewDealsFormattedValues(BaseModel):
    """The formatted values of the deals

    :param currency_id: The formatted values of the deals, defaults to None
    :type currency_id: str, optional
    """

    def __init__(self, currency_id: str = None):
        if currency_id is not None:
            self.currency_id = currency_id


@JsonMap({})
class NewDeals(BaseModel):
    """Deals summary

    :param count: The count of the deals, defaults to None
    :type count: int, optional
    :param deals_ids: The IDs of the deals that have been moved, defaults to None
    :type deals_ids: List[int], optional
    :param values: The values of the deals, defaults to None
    :type values: NewDealsValues, optional
    :param formatted_values: The formatted values of the deals, defaults to None
    :type formatted_values: NewDealsFormattedValues, optional
    """

    def __init__(
        self,
        count: int = None,
        deals_ids: List[int] = None,
        values: NewDealsValues = None,
        formatted_values: NewDealsFormattedValues = None,
    ):
        if count is not None:
            self.count = count
        if deals_ids is not None:
            self.deals_ids = deals_ids
        if values is not None:
            self.values = self._define_object(values, NewDealsValues)
        if formatted_values is not None:
            self.formatted_values = self._define_object(
                formatted_values, NewDealsFormattedValues
            )


@JsonMap({"currency_id": "CURRENCY_ID"})
class DealsLeftOpenValues(BaseModel):
    """The values of the deals

    :param currency_id: The value of the deals, defaults to None
    :type currency_id: int, optional
    """

    def __init__(self, currency_id: int = None):
        if currency_id is not None:
            self.currency_id = currency_id


@JsonMap({"currency_id": "CURRENCY_ID"})
class DealsLeftOpenFormattedValues(BaseModel):
    """The formatted values of the deals

    :param currency_id: The formatted values of the deals, defaults to None
    :type currency_id: str, optional
    """

    def __init__(self, currency_id: str = None):
        if currency_id is not None:
            self.currency_id = currency_id


@JsonMap({})
class DealsLeftOpen(BaseModel):
    """Deals summary

    :param count: The count of the deals, defaults to None
    :type count: int, optional
    :param deals_ids: The IDs of the deals that have been moved, defaults to None
    :type deals_ids: List[int], optional
    :param values: The values of the deals, defaults to None
    :type values: DealsLeftOpenValues, optional
    :param formatted_values: The formatted values of the deals, defaults to None
    :type formatted_values: DealsLeftOpenFormattedValues, optional
    """

    def __init__(
        self,
        count: int = None,
        deals_ids: List[int] = None,
        values: DealsLeftOpenValues = None,
        formatted_values: DealsLeftOpenFormattedValues = None,
    ):
        if count is not None:
            self.count = count
        if deals_ids is not None:
            self.deals_ids = deals_ids
        if values is not None:
            self.values = self._define_object(values, DealsLeftOpenValues)
        if formatted_values is not None:
            self.formatted_values = self._define_object(
                formatted_values, DealsLeftOpenFormattedValues
            )


@JsonMap({"currency_id": "CURRENCY_ID"})
class WonDealsValues(BaseModel):
    """The values of the deals

    :param currency_id: The value of the deals, defaults to None
    :type currency_id: int, optional
    """

    def __init__(self, currency_id: int = None):
        if currency_id is not None:
            self.currency_id = currency_id


@JsonMap({"currency_id": "CURRENCY_ID"})
class WonDealsFormattedValues(BaseModel):
    """The formatted values of the deals

    :param currency_id: The formatted values of the deals, defaults to None
    :type currency_id: str, optional
    """

    def __init__(self, currency_id: str = None):
        if currency_id is not None:
            self.currency_id = currency_id


@JsonMap({})
class WonDeals(BaseModel):
    """Deals summary

    :param count: The count of the deals, defaults to None
    :type count: int, optional
    :param deals_ids: The IDs of the deals that have been moved, defaults to None
    :type deals_ids: List[int], optional
    :param values: The values of the deals, defaults to None
    :type values: WonDealsValues, optional
    :param formatted_values: The formatted values of the deals, defaults to None
    :type formatted_values: WonDealsFormattedValues, optional
    """

    def __init__(
        self,
        count: int = None,
        deals_ids: List[int] = None,
        values: WonDealsValues = None,
        formatted_values: WonDealsFormattedValues = None,
    ):
        if count is not None:
            self.count = count
        if deals_ids is not None:
            self.deals_ids = deals_ids
        if values is not None:
            self.values = self._define_object(values, WonDealsValues)
        if formatted_values is not None:
            self.formatted_values = self._define_object(
                formatted_values, WonDealsFormattedValues
            )


@JsonMap({"currency_id": "CURRENCY_ID"})
class LostDealsValues(BaseModel):
    """The values of the deals

    :param currency_id: The value of the deals, defaults to None
    :type currency_id: int, optional
    """

    def __init__(self, currency_id: int = None):
        if currency_id is not None:
            self.currency_id = currency_id


@JsonMap({"currency_id": "CURRENCY_ID"})
class LostDealsFormattedValues(BaseModel):
    """The formatted values of the deals

    :param currency_id: The formatted values of the deals, defaults to None
    :type currency_id: str, optional
    """

    def __init__(self, currency_id: str = None):
        if currency_id is not None:
            self.currency_id = currency_id


@JsonMap({})
class LostDeals(BaseModel):
    """Deals summary

    :param count: The count of the deals, defaults to None
    :type count: int, optional
    :param deals_ids: The IDs of the deals that have been moved, defaults to None
    :type deals_ids: List[int], optional
    :param values: The values of the deals, defaults to None
    :type values: LostDealsValues, optional
    :param formatted_values: The formatted values of the deals, defaults to None
    :type formatted_values: LostDealsFormattedValues, optional
    """

    def __init__(
        self,
        count: int = None,
        deals_ids: List[int] = None,
        values: LostDealsValues = None,
        formatted_values: LostDealsFormattedValues = None,
    ):
        if count is not None:
            self.count = count
        if deals_ids is not None:
            self.deals_ids = deals_ids
        if values is not None:
            self.values = self._define_object(values, LostDealsValues)
        if formatted_values is not None:
            self.formatted_values = self._define_object(
                formatted_values, LostDealsFormattedValues
            )


@JsonMap({})
class ByStages(BaseModel):
    """The moved deals average age by the stage

    :param stage_id: The stage ID, defaults to None
    :type stage_id: int, optional
    :param value: The average deals age in specific stage, defaults to None
    :type value: int, optional
    """

    def __init__(self, stage_id: int = None, value: int = None):
        if stage_id is not None:
            self.stage_id = stage_id
        if value is not None:
            self.value = value


@JsonMap({})
class AverageAgeInDays(BaseModel):
    """The moved deals average age in days

    :param across_all_stages: The moved deals average age across all stages, defaults to None
    :type across_all_stages: int, optional
    :param by_stages: The moved deals average age by stages, defaults to None
    :type by_stages: List[ByStages], optional
    """

    def __init__(self, across_all_stages: int = None, by_stages: List[ByStages] = None):
        if across_all_stages is not None:
            self.across_all_stages = across_all_stages
        if by_stages is not None:
            self.by_stages = self._define_list(by_stages, ByStages)


@JsonMap({})
class GetPipelineMovementStatisticsOkResponseData(BaseModel):
    """The pipeline object

    :param movements_between_stages: Movements between stages, defaults to None
    :type movements_between_stages: MovementsBetweenStages, optional
    :param new_deals: Deals summary, defaults to None
    :type new_deals: NewDeals, optional
    :param deals_left_open: Deals summary, defaults to None
    :type deals_left_open: DealsLeftOpen, optional
    :param won_deals: Deals summary, defaults to None
    :type won_deals: WonDeals, optional
    :param lost_deals: Deals summary, defaults to None
    :type lost_deals: LostDeals, optional
    :param average_age_in_days: The moved deals average age in days, defaults to None
    :type average_age_in_days: AverageAgeInDays, optional
    """

    def __init__(
        self,
        movements_between_stages: MovementsBetweenStages = None,
        new_deals: NewDeals = None,
        deals_left_open: DealsLeftOpen = None,
        won_deals: WonDeals = None,
        lost_deals: LostDeals = None,
        average_age_in_days: AverageAgeInDays = None,
    ):
        if movements_between_stages is not None:
            self.movements_between_stages = self._define_object(
                movements_between_stages, MovementsBetweenStages
            )
        if new_deals is not None:
            self.new_deals = self._define_object(new_deals, NewDeals)
        if deals_left_open is not None:
            self.deals_left_open = self._define_object(deals_left_open, DealsLeftOpen)
        if won_deals is not None:
            self.won_deals = self._define_object(won_deals, WonDeals)
        if lost_deals is not None:
            self.lost_deals = self._define_object(lost_deals, LostDeals)
        if average_age_in_days is not None:
            self.average_age_in_days = self._define_object(
                average_age_in_days, AverageAgeInDays
            )


@JsonMap({})
class GetPipelineMovementStatisticsOkResponse(BaseModel):
    """GetPipelineMovementStatisticsOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: The pipeline object, defaults to None
    :type data: GetPipelineMovementStatisticsOkResponseData, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: GetPipelineMovementStatisticsOkResponseData = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(
                data, GetPipelineMovementStatisticsOkResponseData
            )
