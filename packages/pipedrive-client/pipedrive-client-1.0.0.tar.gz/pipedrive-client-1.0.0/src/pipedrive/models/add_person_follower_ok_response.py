from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class AddPersonFollowerOkResponseData(BaseModel):
    """AddPersonFollowerOkResponseData

    :param user_id: The ID of the user who was added as a follower to a person, defaults to None
    :type user_id: int, optional
    :param id_: The ID of the follower, defaults to None
    :type id_: int, optional
    :param person_id: The ID of the person to whom the follower was added, defaults to None
    :type person_id: int, optional
    :param add_time: The date and time when the follower was added to a person. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type add_time: str, optional
    """

    def __init__(
        self,
        user_id: int = None,
        id_: int = None,
        person_id: int = None,
        add_time: str = None,
    ):
        if user_id is not None:
            self.user_id = user_id
        if id_ is not None:
            self.id_ = id_
        if person_id is not None:
            self.person_id = person_id
        if add_time is not None:
            self.add_time = add_time


@JsonMap({})
class AddPersonFollowerOkResponse(BaseModel):
    """AddPersonFollowerOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: AddPersonFollowerOkResponseData, optional
    """

    def __init__(
        self, success: bool = None, data: AddPersonFollowerOkResponseData = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, AddPersonFollowerOkResponseData)
