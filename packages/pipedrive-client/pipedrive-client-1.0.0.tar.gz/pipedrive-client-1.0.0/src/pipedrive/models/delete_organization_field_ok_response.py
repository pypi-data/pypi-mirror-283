from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class DeleteOrganizationFieldOkResponseData(BaseModel):
    """DeleteOrganizationFieldOkResponseData

    :param id_: The ID of the field that was deleted, defaults to None
    :type id_: int, optional
    """

    def __init__(self, id_: int = None):
        if id_ is not None:
            self.id_ = id_


@JsonMap({})
class DeleteOrganizationFieldOkResponse(BaseModel):
    """DeleteOrganizationFieldOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: DeleteOrganizationFieldOkResponseData, optional
    """

    def __init__(
        self, success: bool = None, data: DeleteOrganizationFieldOkResponseData = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, DeleteOrganizationFieldOkResponseData)
