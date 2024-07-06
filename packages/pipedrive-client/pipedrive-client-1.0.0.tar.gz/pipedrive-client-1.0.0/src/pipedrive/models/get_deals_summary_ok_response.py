from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class ValuesTotal(BaseModel):
    """The total values of the deals grouped by deal currency

    :param value: The total value of deals in the deal currency group, defaults to None
    :type value: float, optional
    :param count: The number of deals in the deal currency group, defaults to None
    :type count: int, optional
    :param value_converted: The total value of deals converted into the company default currency, defaults to None
    :type value_converted: float, optional
    :param value_formatted: The total value of deals formatted with deal currency. E.g. €50, defaults to None
    :type value_formatted: str, optional
    :param value_converted_formatted: The value_converted formatted with deal currency. E.g. US$50.10, defaults to None
    :type value_converted_formatted: str, optional
    """

    def __init__(
        self,
        value: float = None,
        count: int = None,
        value_converted: float = None,
        value_formatted: str = None,
        value_converted_formatted: str = None,
    ):
        if value is not None:
            self.value = value
        if count is not None:
            self.count = count
        if value_converted is not None:
            self.value_converted = value_converted
        if value_formatted is not None:
            self.value_formatted = value_formatted
        if value_converted_formatted is not None:
            self.value_converted_formatted = value_converted_formatted


@JsonMap({})
class WeightedValuesTotal(BaseModel):
    """The total weighted values of the deals grouped by deal currency. The weighted value is calculated as probability times deal value.

    :param value: The total weighted value of the deals in the deal currency group, defaults to None
    :type value: float, optional
    :param count: The number of deals in the deal currency group, defaults to None
    :type count: int, optional
    :param value_formatted: The total weighted value of the deals formatted with deal currency. E.g. €50, defaults to None
    :type value_formatted: str, optional
    """

    def __init__(
        self, value: float = None, count: int = None, value_formatted: str = None
    ):
        if value is not None:
            self.value = value
        if count is not None:
            self.count = count
        if value_formatted is not None:
            self.value_formatted = value_formatted


@JsonMap({})
class GetDealsSummaryOkResponseData(BaseModel):
    """The summary of deals

    :param values_total: The total values of the deals grouped by deal currency, defaults to None
    :type values_total: ValuesTotal, optional
    :param weighted_values_total: The total weighted values of the deals grouped by deal currency. The weighted value is calculated as probability times deal value., defaults to None
    :type weighted_values_total: WeightedValuesTotal, optional
    :param total_count: The total number of deals, defaults to None
    :type total_count: int, optional
    :param total_currency_converted_value: The total value of deals converted into the company default currency, defaults to None
    :type total_currency_converted_value: float, optional
    :param total_weighted_currency_converted_value: The total weighted value of deals converted into the company default currency, defaults to None
    :type total_weighted_currency_converted_value: float, optional
    :param total_currency_converted_value_formatted: The total converted value of deals formatted with the company default currency. E.g. US$5,100.96, defaults to None
    :type total_currency_converted_value_formatted: str, optional
    :param total_weighted_currency_converted_value_formatted: The total weighted value of deals formatted with the company default currency. E.g. US$5,100.96, defaults to None
    :type total_weighted_currency_converted_value_formatted: str, optional
    """

    def __init__(
        self,
        values_total: ValuesTotal = None,
        weighted_values_total: WeightedValuesTotal = None,
        total_count: int = None,
        total_currency_converted_value: float = None,
        total_weighted_currency_converted_value: float = None,
        total_currency_converted_value_formatted: str = None,
        total_weighted_currency_converted_value_formatted: str = None,
    ):
        if values_total is not None:
            self.values_total = self._define_object(values_total, ValuesTotal)
        if weighted_values_total is not None:
            self.weighted_values_total = self._define_object(
                weighted_values_total, WeightedValuesTotal
            )
        if total_count is not None:
            self.total_count = total_count
        if total_currency_converted_value is not None:
            self.total_currency_converted_value = total_currency_converted_value
        if total_weighted_currency_converted_value is not None:
            self.total_weighted_currency_converted_value = (
                total_weighted_currency_converted_value
            )
        if total_currency_converted_value_formatted is not None:
            self.total_currency_converted_value_formatted = (
                total_currency_converted_value_formatted
            )
        if total_weighted_currency_converted_value_formatted is not None:
            self.total_weighted_currency_converted_value_formatted = (
                total_weighted_currency_converted_value_formatted
            )


@JsonMap({})
class GetDealsSummaryOkResponse(BaseModel):
    """GetDealsSummaryOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: The summary of deals, defaults to None
    :type data: GetDealsSummaryOkResponseData, optional
    """

    def __init__(
        self, success: bool = None, data: GetDealsSummaryOkResponseData = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, GetDealsSummaryOkResponseData)
