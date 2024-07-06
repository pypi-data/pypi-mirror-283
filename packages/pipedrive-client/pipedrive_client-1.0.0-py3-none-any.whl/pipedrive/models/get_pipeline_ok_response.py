from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class StageIdCurrencyId1(BaseModel):
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
class PerStagesStageId1(BaseModel):
    """The currency summaries per stage. This parameter is dynamic and changes according to `stage_id` value.

    :param currency_id: The currency summary. This parameter is dynamic and changes according to `currency_id` value., defaults to None
    :type currency_id: StageIdCurrencyId1, optional
    """

    def __init__(self, currency_id: StageIdCurrencyId1 = None):
        if currency_id is not None:
            self.currency_id = self._define_object(currency_id, StageIdCurrencyId1)


@JsonMap({"stage_id": "STAGE_ID"})
class DealsSummaryPerStages1(BaseModel):
    """The stage objects containing deals currency information

    :param stage_id: The currency summaries per stage. This parameter is dynamic and changes according to `stage_id` value., defaults to None
    :type stage_id: PerStagesStageId1, optional
    """

    def __init__(self, stage_id: PerStagesStageId1 = None):
        if stage_id is not None:
            self.stage_id = self._define_object(stage_id, PerStagesStageId1)


@JsonMap({"currency_id": "CURRENCY_ID"})
class DealsSummaryPerCurrency1(BaseModel):
    """The currency count summary

    :param currency_id: Deals count per currency. This parameter is dynamic and changes according to `currency_id` value., defaults to None
    :type currency_id: int, optional
    """

    def __init__(self, currency_id: int = None):
        if currency_id is not None:
            self.currency_id = currency_id


@JsonMap({})
class PerCurrencyFullCurrencyId1(BaseModel):
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
class DealsSummaryPerCurrencyFull1(BaseModel):
    """Full currency summaries

    :param currency_id: The currency summary. This parameter is dynamic and changes according to `currency_id` value., defaults to None
    :type currency_id: PerCurrencyFullCurrencyId1, optional
    """

    def __init__(self, currency_id: PerCurrencyFullCurrencyId1 = None):
        if currency_id is not None:
            self.currency_id = self._define_object(
                currency_id, PerCurrencyFullCurrencyId1
            )


@JsonMap({})
class DataDealsSummary1(BaseModel):
    """Deals summary

    :param per_stages: The stage objects containing deals currency information, defaults to None
    :type per_stages: DealsSummaryPerStages1, optional
    :param per_currency: The currency count summary, defaults to None
    :type per_currency: DealsSummaryPerCurrency1, optional
    :param total_count: Deals count, defaults to None
    :type total_count: int, optional
    :param per_currency_full: Full currency summaries, defaults to None
    :type per_currency_full: DealsSummaryPerCurrencyFull1, optional
    """

    def __init__(
        self,
        per_stages: DealsSummaryPerStages1 = None,
        per_currency: DealsSummaryPerCurrency1 = None,
        total_count: int = None,
        per_currency_full: DealsSummaryPerCurrencyFull1 = None,
    ):
        if per_stages is not None:
            self.per_stages = self._define_object(per_stages, DealsSummaryPerStages1)
        if per_currency is not None:
            self.per_currency = self._define_object(
                per_currency, DealsSummaryPerCurrency1
            )
        if total_count is not None:
            self.total_count = total_count
        if per_currency_full is not None:
            self.per_currency_full = self._define_object(
                per_currency_full, DealsSummaryPerCurrencyFull1
            )


@JsonMap({"id_": "id"})
class GetPipelineOkResponseData(BaseModel):
    """GetPipelineOkResponseData

    :param id_: The ID of the pipeline, defaults to None
    :type id_: int, optional
    :param name: The name of the pipeline, defaults to None
    :type name: str, optional
    :param url_title: The pipeline title displayed in the URL, defaults to None
    :type url_title: str, optional
    :param order_nr: Defines the order of pipelines. First order (`order_nr=0`) is the default pipeline., defaults to None
    :type order_nr: int, optional
    :param active: Whether this pipeline will be made inactive (hidden) or active, defaults to None
    :type active: bool, optional
    :param deal_probability: Whether deal probability is disabled or enabled for this pipeline, defaults to None
    :type deal_probability: bool, optional
    :param add_time: The pipeline creation time. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type add_time: str, optional
    :param update_time: The pipeline update time. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type update_time: str, optional
    :param selected: A boolean that shows if the pipeline is selected from a filter or not, defaults to None
    :type selected: bool, optional
    :param deals_summary: Deals summary, defaults to None
    :type deals_summary: DataDealsSummary1, optional
    """

    def __init__(
        self,
        id_: int = None,
        name: str = None,
        url_title: str = None,
        order_nr: int = None,
        active: bool = None,
        deal_probability: bool = None,
        add_time: str = None,
        update_time: str = None,
        selected: bool = None,
        deals_summary: DataDealsSummary1 = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if url_title is not None:
            self.url_title = url_title
        if order_nr is not None:
            self.order_nr = order_nr
        if active is not None:
            self.active = active
        if deal_probability is not None:
            self.deal_probability = deal_probability
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time
        if selected is not None:
            self.selected = selected
        if deals_summary is not None:
            self.deals_summary = self._define_object(deals_summary, DataDealsSummary1)


@JsonMap({})
class GetPipelineOkResponse(BaseModel):
    """GetPipelineOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: GetPipelineOkResponseData, optional
    """

    def __init__(self, success: bool = None, data: GetPipelineOkResponseData = None):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, GetPipelineOkResponseData)
