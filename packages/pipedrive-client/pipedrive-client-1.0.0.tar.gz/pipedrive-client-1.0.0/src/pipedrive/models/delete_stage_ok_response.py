from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class DeleteStageOkResponseData(BaseModel):
    """DeleteStageOkResponseData

    :param id_: Deleted stage ID, defaults to None
    :type id_: int, optional
    """

    def __init__(self, id_: int = None):
        if id_ is not None:
            self.id_ = id_


@JsonMap({})
class DeleteStageOkResponse(BaseModel):
    """DeleteStageOkResponse

    :param success: If the request was successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: DeleteStageOkResponseData, optional
    """

    def __init__(self, success: bool = None, data: DeleteStageOkResponseData = None):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, DeleteStageOkResponseData)
