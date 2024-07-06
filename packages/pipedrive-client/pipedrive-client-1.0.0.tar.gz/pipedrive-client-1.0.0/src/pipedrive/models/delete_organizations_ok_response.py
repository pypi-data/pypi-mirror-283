from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class DeleteOrganizationsOkResponseData(BaseModel):
    """DeleteOrganizationsOkResponseData

    :param id_: The IDs of the organizations that were deleted, defaults to None
    :type id_: List[float], optional
    """

    def __init__(self, id_: List[float] = None):
        if id_ is not None:
            self.id_ = id_


@JsonMap({})
class DeleteOrganizationsOkResponse(BaseModel):
    """DeleteOrganizationsOkResponse

    :param success: If the request was successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: DeleteOrganizationsOkResponseData, optional
    """

    def __init__(
        self, success: bool = None, data: DeleteOrganizationsOkResponseData = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, DeleteOrganizationsOkResponseData)
