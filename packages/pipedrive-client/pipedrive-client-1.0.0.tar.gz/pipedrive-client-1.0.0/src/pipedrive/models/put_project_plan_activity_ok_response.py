from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class PutProjectPlanActivityOkResponseData(BaseModel):
    """PutProjectPlanActivityOkResponseData

    :param item_id: ID of plan item (either activity or task ID), defaults to None
    :type item_id: float, optional
    :param item_type: Type of a plan item (task / activity), defaults to None
    :type item_type: str, optional
    :param phase_id: The ID of the board this project is associated with. If null then plan item is not in any phase., defaults to None
    :type phase_id: float, optional
    :param group_id: The ID of the board this project is associated with. If null then plan item is not in any group., defaults to None
    :type group_id: float, optional
    """

    def __init__(
        self,
        item_id: float = None,
        item_type: str = None,
        phase_id: float = None,
        group_id: float = None,
    ):
        if item_id is not None:
            self.item_id = item_id
        if item_type is not None:
            self.item_type = item_type
        if phase_id is not None:
            self.phase_id = phase_id
        if group_id is not None:
            self.group_id = group_id


@JsonMap({})
class PutProjectPlanActivityOkResponse(BaseModel):
    """PutProjectPlanActivityOkResponse

    :param success: success, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: PutProjectPlanActivityOkResponseData, optional
    :param additional_data: additional_data, defaults to None
    :type additional_data: dict, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: PutProjectPlanActivityOkResponseData = None,
        additional_data: dict = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, PutProjectPlanActivityOkResponseData)
        if additional_data is not None:
            self.additional_data = additional_data
