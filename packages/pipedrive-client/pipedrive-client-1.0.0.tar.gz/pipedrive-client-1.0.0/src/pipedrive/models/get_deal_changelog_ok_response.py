from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class GetDealChangelogOkResponseData(BaseModel):
    """GetDealChangelogOkResponseData

    :param field_key: The key of the field that was changed, defaults to None
    :type field_key: str, optional
    :param old_value: The value of the field before the change, defaults to None
    :type old_value: str, optional
    :param new_value: The value of the field after the change, defaults to None
    :type new_value: str, optional
    :param actor_user_id: The ID of the user who made the change, defaults to None
    :type actor_user_id: int, optional
    :param time: The date and time of the change, defaults to None
    :type time: str, optional
    :param change_source: The source of change, for example 'app', 'mobile', 'api', etc., defaults to None
    :type change_source: str, optional
    :param change_source_user_agent: The user agent from which the change was made, defaults to None
    :type change_source_user_agent: str, optional
    :param is_bulk_update_flag: Whether the change was made as part of a bulk update, defaults to None
    :type is_bulk_update_flag: bool, optional
    """

    def __init__(
        self,
        field_key: str = None,
        old_value: str = None,
        new_value: str = None,
        actor_user_id: int = None,
        time: str = None,
        change_source: str = None,
        change_source_user_agent: str = None,
        is_bulk_update_flag: bool = None,
    ):
        if field_key is not None:
            self.field_key = field_key
        if old_value is not None:
            self.old_value = old_value
        if new_value is not None:
            self.new_value = new_value
        if actor_user_id is not None:
            self.actor_user_id = actor_user_id
        if time is not None:
            self.time = time
        if change_source is not None:
            self.change_source = change_source
        if change_source_user_agent is not None:
            self.change_source_user_agent = change_source_user_agent
        if is_bulk_update_flag is not None:
            self.is_bulk_update_flag = is_bulk_update_flag


@JsonMap({})
class GetDealChangelogOkResponseAdditionalData(BaseModel):
    """The additional data of the list

    :param next_cursor: The first item on the next page. The value of the `next_cursor` field will be `null` if you have reached the end of the dataset and there’s no more pages to be returned., defaults to None
    :type next_cursor: str, optional
    """

    def __init__(self, next_cursor: str = None):
        if next_cursor is not None:
            self.next_cursor = next_cursor


@JsonMap({})
class GetDealChangelogOkResponse(BaseModel):
    """GetDealChangelogOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: List[GetDealChangelogOkResponseData], optional
    :param additional_data: The additional data of the list, defaults to None
    :type additional_data: GetDealChangelogOkResponseAdditionalData, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: List[GetDealChangelogOkResponseData] = None,
        additional_data: GetDealChangelogOkResponseAdditionalData = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(data, GetDealChangelogOkResponseData)
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, GetDealChangelogOkResponseAdditionalData
            )
