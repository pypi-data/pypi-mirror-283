from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class DeletePersonFieldOkResponseData(BaseModel):
    """DeletePersonFieldOkResponseData

    :param id_: The ID of the field that was deleted, defaults to None
    :type id_: int, optional
    """

    def __init__(self, id_: int = None):
        if id_ is not None:
            self.id_ = id_


@JsonMap({})
class DeletePersonFieldOkResponse(BaseModel):
    """DeletePersonFieldOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: DeletePersonFieldOkResponseData, optional
    """

    def __init__(
        self, success: bool = None, data: DeletePersonFieldOkResponseData = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, DeletePersonFieldOkResponseData)
