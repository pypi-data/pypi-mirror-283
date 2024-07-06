from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class GetCurrenciesOkResponseData(BaseModel):
    """GetCurrenciesOkResponseData

    :param id_: The ID of the currency, defaults to None
    :type id_: int, optional
    :param code: The code of the currency, defaults to None
    :type code: str, optional
    :param name: The name of the currency, defaults to None
    :type name: str, optional
    :param decimal_points: The amount of decimal points of the currency, defaults to None
    :type decimal_points: int, optional
    :param symbol: The symbol of the currency, defaults to None
    :type symbol: str, optional
    :param active_flag: Whether the currency is active or not, defaults to None
    :type active_flag: bool, optional
    :param is_custom_flag: Whether the currency is a custom one or not, defaults to None
    :type is_custom_flag: bool, optional
    """

    def __init__(
        self,
        id_: int = None,
        code: str = None,
        name: str = None,
        decimal_points: int = None,
        symbol: str = None,
        active_flag: bool = None,
        is_custom_flag: bool = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if code is not None:
            self.code = code
        if name is not None:
            self.name = name
        if decimal_points is not None:
            self.decimal_points = decimal_points
        if symbol is not None:
            self.symbol = symbol
        if active_flag is not None:
            self.active_flag = active_flag
        if is_custom_flag is not None:
            self.is_custom_flag = is_custom_flag


@JsonMap({})
class GetCurrenciesOkResponse(BaseModel):
    """GetCurrenciesOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: The array of currencies, defaults to None
    :type data: List[GetCurrenciesOkResponseData], optional
    """

    def __init__(
        self, success: bool = None, data: List[GetCurrenciesOkResponseData] = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(data, GetCurrenciesOkResponseData)
