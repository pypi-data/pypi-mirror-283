from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class AddOrganizationFollowerOkResponseData(BaseModel):
    """AddOrganizationFollowerOkResponseData

    :param org_id: The ID of the organization, defaults to None
    :type org_id: int, optional
    :param user_id: The user ID of the follower related to the item, defaults to None
    :type user_id: int, optional
    :param id_: The ID of the follower, defaults to None
    :type id_: int, optional
    :param add_time: The date and time of adding the follower to the item, defaults to None
    :type add_time: str, optional
    """

    def __init__(
        self,
        org_id: int = None,
        user_id: int = None,
        id_: int = None,
        add_time: str = None,
    ):
        if org_id is not None:
            self.org_id = org_id
        if user_id is not None:
            self.user_id = user_id
        if id_ is not None:
            self.id_ = id_
        if add_time is not None:
            self.add_time = add_time


@JsonMap({})
class AddOrganizationFollowerOkResponse(BaseModel):
    """AddOrganizationFollowerOkResponse

    :param success: If the request was successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: AddOrganizationFollowerOkResponseData, optional
    """

    def __init__(
        self, success: bool = None, data: AddOrganizationFollowerOkResponseData = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, AddOrganizationFollowerOkResponseData)
