from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class DeleteProductFollowerOkResponseData(BaseModel):
    """DeleteProductFollowerOkResponseData

    :param id_: id_, defaults to None
    :type id_: int, optional
    """

    def __init__(self, id_: int = None):
        if id_ is not None:
            self.id_ = id_


@JsonMap({})
class DeleteProductFollowerOkResponse(BaseModel):
    """DeleteProductFollowerOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: DeleteProductFollowerOkResponseData, optional
    """

    def __init__(
        self, success: bool = None, data: DeleteProductFollowerOkResponseData = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, DeleteProductFollowerOkResponseData)
