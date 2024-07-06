from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class DataData6(BaseModel):
    """DataData6

    :param id_: The ID of the task that was deleted, defaults to None
    :type id_: int, optional
    """

    def __init__(self, id_: int = None):
        if id_ is not None:
            self.id_ = id_


@JsonMap({})
class DeleteTaskOkResponseData(BaseModel):
    """DeleteTaskOkResponseData

    :param success: If the request was successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: DataData6, optional
    """

    def __init__(self, success: bool = None, data: DataData6 = None):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, DataData6)


@JsonMap({})
class DeleteTaskOkResponse(BaseModel):
    """DeleteTaskOkResponse

    :param success: success, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: DeleteTaskOkResponseData, optional
    :param additional_data: additional_data, defaults to None
    :type additional_data: dict, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: DeleteTaskOkResponseData = None,
        additional_data: dict = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, DeleteTaskOkResponseData)
        if additional_data is not None:
            self.additional_data = additional_data
