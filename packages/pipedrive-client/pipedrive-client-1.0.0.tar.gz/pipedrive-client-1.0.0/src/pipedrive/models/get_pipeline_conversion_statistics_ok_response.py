from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class StageConversions(BaseModel):
    """StageConversions

    :param from_stage_id: The stage ID from where conversion starts, defaults to None
    :type from_stage_id: int, optional
    :param to_stage_id: The stage ID to where conversion ends, defaults to None
    :type to_stage_id: int, optional
    :param conversion_rate: The conversion rate, defaults to None
    :type conversion_rate: int, optional
    """

    def __init__(
        self,
        from_stage_id: int = None,
        to_stage_id: int = None,
        conversion_rate: int = None,
    ):
        if from_stage_id is not None:
            self.from_stage_id = from_stage_id
        if to_stage_id is not None:
            self.to_stage_id = to_stage_id
        if conversion_rate is not None:
            self.conversion_rate = conversion_rate


@JsonMap({})
class GetPipelineConversionStatisticsOkResponseData(BaseModel):
    """The pipeline object

    :param stage_conversions: The stage conversions, defaults to None
    :type stage_conversions: List[StageConversions], optional
    :param won_conversion: The won conversion, defaults to None
    :type won_conversion: int, optional
    :param lost_conversion: The lost conversion, defaults to None
    :type lost_conversion: int, optional
    """

    def __init__(
        self,
        stage_conversions: List[StageConversions] = None,
        won_conversion: int = None,
        lost_conversion: int = None,
    ):
        if stage_conversions is not None:
            self.stage_conversions = self._define_list(
                stage_conversions, StageConversions
            )
        if won_conversion is not None:
            self.won_conversion = won_conversion
        if lost_conversion is not None:
            self.lost_conversion = lost_conversion


@JsonMap({})
class GetPipelineConversionStatisticsOkResponse(BaseModel):
    """GetPipelineConversionStatisticsOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: The pipeline object, defaults to None
    :type data: GetPipelineConversionStatisticsOkResponseData, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: GetPipelineConversionStatisticsOkResponseData = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(
                data, GetPipelineConversionStatisticsOkResponseData
            )
