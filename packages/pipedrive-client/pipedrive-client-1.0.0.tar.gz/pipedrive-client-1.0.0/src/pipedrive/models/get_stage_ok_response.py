from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class StageIdCurrencyId2(BaseModel):
    """The currency summary. This parameter is dynamic and changes according to `currency_id` value.

    :param count: Deals count per currency, defaults to None
    :type count: int, optional
    :param value: Deals value per currency, defaults to None
    :type value: int, optional
    :param value_formatted: Deals value formatted per currency, defaults to None
    :type value_formatted: str, optional
    :param weighted_value: Deals weighted value per currency, defaults to None
    :type weighted_value: int, optional
    :param weighted_value_formatted: Deals weighted value formatted per currency, defaults to None
    :type weighted_value_formatted: str, optional
    """

    def __init__(
        self,
        count: int = None,
        value: int = None,
        value_formatted: str = None,
        weighted_value: int = None,
        weighted_value_formatted: str = None,
    ):
        if count is not None:
            self.count = count
        if value is not None:
            self.value = value
        if value_formatted is not None:
            self.value_formatted = value_formatted
        if weighted_value is not None:
            self.weighted_value = weighted_value
        if weighted_value_formatted is not None:
            self.weighted_value_formatted = weighted_value_formatted


@JsonMap({"currency_id": "CURRENCY_ID"})
class PerStagesStageId2(BaseModel):
    """The currency summaries per stage. This parameter is dynamic and changes according to `stage_id` value.

    :param currency_id: The currency summary. This parameter is dynamic and changes according to `currency_id` value., defaults to None
    :type currency_id: StageIdCurrencyId2, optional
    """

    def __init__(self, currency_id: StageIdCurrencyId2 = None):
        if currency_id is not None:
            self.currency_id = self._define_object(currency_id, StageIdCurrencyId2)


@JsonMap({"stage_id": "STAGE_ID"})
class DealsSummaryPerStages2(BaseModel):
    """The stage objects containing deals currency information

    :param stage_id: The currency summaries per stage. This parameter is dynamic and changes according to `stage_id` value., defaults to None
    :type stage_id: PerStagesStageId2, optional
    """

    def __init__(self, stage_id: PerStagesStageId2 = None):
        if stage_id is not None:
            self.stage_id = self._define_object(stage_id, PerStagesStageId2)


@JsonMap({"currency_id": "CURRENCY_ID"})
class DealsSummaryPerCurrency2(BaseModel):
    """The currency count summary

    :param currency_id: Deals count per currency. This parameter is dynamic and changes according to `currency_id` value., defaults to None
    :type currency_id: int, optional
    """

    def __init__(self, currency_id: int = None):
        if currency_id is not None:
            self.currency_id = currency_id


@JsonMap({})
class PerCurrencyFullCurrencyId2(BaseModel):
    """The currency summary. This parameter is dynamic and changes according to `currency_id` value.

    :param count: Deals count per currency, defaults to None
    :type count: int, optional
    :param value: Deals value per currency, defaults to None
    :type value: int, optional
    """

    def __init__(self, count: int = None, value: int = None):
        if count is not None:
            self.count = count
        if value is not None:
            self.value = value


@JsonMap({"currency_id": "CURRENCY_ID"})
class DealsSummaryPerCurrencyFull2(BaseModel):
    """Full currency summaries

    :param currency_id: The currency summary. This parameter is dynamic and changes according to `currency_id` value., defaults to None
    :type currency_id: PerCurrencyFullCurrencyId2, optional
    """

    def __init__(self, currency_id: PerCurrencyFullCurrencyId2 = None):
        if currency_id is not None:
            self.currency_id = self._define_object(
                currency_id, PerCurrencyFullCurrencyId2
            )


@JsonMap({})
class DataDealsSummary2(BaseModel):
    """Deals summary

    :param per_stages: The stage objects containing deals currency information, defaults to None
    :type per_stages: DealsSummaryPerStages2, optional
    :param per_currency: The currency count summary, defaults to None
    :type per_currency: DealsSummaryPerCurrency2, optional
    :param total_count: Deals count, defaults to None
    :type total_count: int, optional
    :param per_currency_full: Full currency summaries, defaults to None
    :type per_currency_full: DealsSummaryPerCurrencyFull2, optional
    """

    def __init__(
        self,
        per_stages: DealsSummaryPerStages2 = None,
        per_currency: DealsSummaryPerCurrency2 = None,
        total_count: int = None,
        per_currency_full: DealsSummaryPerCurrencyFull2 = None,
    ):
        if per_stages is not None:
            self.per_stages = self._define_object(per_stages, DealsSummaryPerStages2)
        if per_currency is not None:
            self.per_currency = self._define_object(
                per_currency, DealsSummaryPerCurrency2
            )
        if total_count is not None:
            self.total_count = total_count
        if per_currency_full is not None:
            self.per_currency_full = self._define_object(
                per_currency_full, DealsSummaryPerCurrencyFull2
            )


@JsonMap({"id_": "id"})
class GetStageOkResponseData(BaseModel):
    """GetStageOkResponseData

    :param id_: The ID of the stage, defaults to None
    :type id_: int, optional
    :param order_nr: Defines the order of the stage, defaults to None
    :type order_nr: int, optional
    :param name: The name of the stage, defaults to None
    :type name: str, optional
    :param active_flag: Whether the stage is active or deleted, defaults to None
    :type active_flag: bool, optional
    :param deal_probability: The success probability percentage of the deal. Used/shown when the deal weighted values are used., defaults to None
    :type deal_probability: int, optional
    :param pipeline_id: The ID of the pipeline to add the stage to, defaults to None
    :type pipeline_id: int, optional
    :param rotten_flag: Whether deals in this stage can become rotten, defaults to None
    :type rotten_flag: bool, optional
    :param rotten_days: The number of days the deals not updated in this stage would become rotten. Applies only if the `rotten_flag` is set., defaults to None
    :type rotten_days: int, optional
    :param add_time: The stage creation time. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type add_time: str, optional
    :param update_time: The stage update time. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type update_time: str, optional
    :param deals_summary: Deals summary, defaults to None
    :type deals_summary: DataDealsSummary2, optional
    """

    def __init__(
        self,
        id_: int = None,
        order_nr: int = None,
        name: str = None,
        active_flag: bool = None,
        deal_probability: int = None,
        pipeline_id: int = None,
        rotten_flag: bool = None,
        rotten_days: int = None,
        add_time: str = None,
        update_time: str = None,
        deals_summary: DataDealsSummary2 = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if order_nr is not None:
            self.order_nr = order_nr
        if name is not None:
            self.name = name
        if active_flag is not None:
            self.active_flag = active_flag
        if deal_probability is not None:
            self.deal_probability = deal_probability
        if pipeline_id is not None:
            self.pipeline_id = pipeline_id
        if rotten_flag is not None:
            self.rotten_flag = rotten_flag
        if rotten_days is not None:
            self.rotten_days = rotten_days
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time
        if deals_summary is not None:
            self.deals_summary = self._define_object(deals_summary, DataDealsSummary2)


@JsonMap({})
class GetStageOkResponse(BaseModel):
    """GetStageOkResponse

    :param success: If the request was successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: GetStageOkResponseData, optional
    """

    def __init__(self, success: bool = None, data: GetStageOkResponseData = None):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, GetStageOkResponseData)
