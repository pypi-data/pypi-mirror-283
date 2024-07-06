from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class DataData5(BaseModel):
    """DataData5

    :param id_: The ID of the project that was deleted, defaults to None
    :type id_: int, optional
    """

    def __init__(self, id_: int = None):
        if id_ is not None:
            self.id_ = id_


@JsonMap({})
class DeleteProjectOkResponseData(BaseModel):
    """DeleteProjectOkResponseData

    :param success: If the request was successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: DataData5, optional
    """

    def __init__(self, success: bool = None, data: DataData5 = None):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, DataData5)


@JsonMap({})
class DeleteProjectOkResponse(BaseModel):
    """DeleteProjectOkResponse

    :param success: success, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: DeleteProjectOkResponseData, optional
    :param additional_data: additional_data, defaults to None
    :type additional_data: dict, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: DeleteProjectOkResponseData = None,
        additional_data: dict = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, DeleteProjectOkResponseData)
        if additional_data is not None:
            self.additional_data = additional_data
