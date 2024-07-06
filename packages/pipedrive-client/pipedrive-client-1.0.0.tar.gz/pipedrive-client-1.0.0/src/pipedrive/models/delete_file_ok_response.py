from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class DeleteFileOkResponseData(BaseModel):
    """DeleteFileOkResponseData

    :param id_: The ID of the file, defaults to None
    :type id_: int, optional
    """

    def __init__(self, id_: int = None):
        if id_ is not None:
            self.id_ = id_


@JsonMap({})
class DeleteFileOkResponse(BaseModel):
    """DeleteFileOkResponse

    :param success: If the request was successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: DeleteFileOkResponseData, optional
    """

    def __init__(self, success: bool = None, data: DeleteFileOkResponseData = None):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, DeleteFileOkResponseData)
