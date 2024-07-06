from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id", "type_": "type"})
class GetFilterOkResponseData(BaseModel):
    """The filter object

    :param id_: The ID of the filter, defaults to None
    :type id_: int, optional
    :param name: The name of the filter, defaults to None
    :type name: str, optional
    :param active_flag: The active flag of the filter, defaults to None
    :type active_flag: bool, optional
    :param type_: The type of the item, defaults to None
    :type type_: str, optional
    :param user_id: The owner of the filter, defaults to None
    :type user_id: int, optional
    :param add_time: The date and time when the filter was added, defaults to None
    :type add_time: str, optional
    :param update_time: The date and time when the filter was updated, defaults to None
    :type update_time: str, optional
    :param visible_to: The visibility group ID of who can see then filter, defaults to None
    :type visible_to: int, optional
    :param custom_view_id: Used by Pipedrive webapp, defaults to None
    :type custom_view_id: int, optional
    """

    def __init__(
        self,
        id_: int = None,
        name: str = None,
        active_flag: bool = None,
        type_: str = None,
        user_id: int = None,
        add_time: str = None,
        update_time: str = None,
        visible_to: int = None,
        custom_view_id: int = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if active_flag is not None:
            self.active_flag = active_flag
        if type_ is not None:
            self.type_ = type_
        if user_id is not None:
            self.user_id = user_id
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time
        if visible_to is not None:
            self.visible_to = visible_to
        if custom_view_id is not None:
            self.custom_view_id = custom_view_id


@JsonMap({})
class GetFilterOkResponse(BaseModel):
    """GetFilterOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: The filter object, defaults to None
    :type data: GetFilterOkResponseData, optional
    """

    def __init__(self, success: bool = None, data: GetFilterOkResponseData = None):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, GetFilterOkResponseData)
