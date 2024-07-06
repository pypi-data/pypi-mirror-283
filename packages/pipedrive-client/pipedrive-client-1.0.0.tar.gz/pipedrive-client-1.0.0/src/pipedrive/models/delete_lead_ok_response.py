from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class DeleteLeadOkResponseData(BaseModel):
    """DeleteLeadOkResponseData

    :param id_: id_, defaults to None
    :type id_: str, optional
    """

    def __init__(self, id_: str = None):
        if id_ is not None:
            self.id_ = id_


@JsonMap({})
class DeleteLeadOkResponse(BaseModel):
    """DeleteLeadOkResponse

    :param success: success, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: DeleteLeadOkResponseData, optional
    """

    def __init__(self, success: bool = None, data: DeleteLeadOkResponseData = None):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, DeleteLeadOkResponseData)
