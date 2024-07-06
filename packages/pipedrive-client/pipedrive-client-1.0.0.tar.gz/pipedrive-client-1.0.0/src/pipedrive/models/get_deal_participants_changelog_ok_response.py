from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class GetDealParticipantsChangelogOkResponseData(BaseModel):
    """GetDealParticipantsChangelogOkResponseData

    :param actor_user_id: The ID of the user, defaults to None
    :type actor_user_id: int, optional
    :param person_id: The ID of the person, defaults to None
    :type person_id: int, optional
    :param action: Deal participant action type, defaults to None
    :type action: str, optional
    :param time: The deal participant action log time, defaults to None
    :type time: str, optional
    """

    def __init__(
        self,
        actor_user_id: int = None,
        person_id: int = None,
        action: str = None,
        time: str = None,
    ):
        if actor_user_id is not None:
            self.actor_user_id = actor_user_id
        if person_id is not None:
            self.person_id = person_id
        if action is not None:
            self.action = action
        if time is not None:
            self.time = time


@JsonMap({})
class GetDealParticipantsChangelogOkResponseAdditionalData(BaseModel):
    """The additional data of the list

    :param start: Pagination start, defaults to None
    :type start: int, optional
    :param limit: Items shown per page, defaults to None
    :type limit: int, optional
    :param more_items_in_collection: If there are more list items in the collection than displayed or not, defaults to None
    :type more_items_in_collection: bool, optional
    """

    def __init__(
        self,
        start: int = None,
        limit: int = None,
        more_items_in_collection: bool = None,
    ):
        if start is not None:
            self.start = start
        if limit is not None:
            self.limit = limit
        if more_items_in_collection is not None:
            self.more_items_in_collection = more_items_in_collection


@JsonMap({})
class GetDealParticipantsChangelogOkResponse(BaseModel):
    """GetDealParticipantsChangelogOkResponse

    :param success: If the request was successful or not, defaults to None
    :type success: bool, optional
    :param data: The array of participant changelog, defaults to None
    :type data: List[GetDealParticipantsChangelogOkResponseData], optional
    :param additional_data: The additional data of the list, defaults to None
    :type additional_data: GetDealParticipantsChangelogOkResponseAdditionalData, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: List[GetDealParticipantsChangelogOkResponseData] = None,
        additional_data: GetDealParticipantsChangelogOkResponseAdditionalData = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(
                data, GetDealParticipantsChangelogOkResponseData
            )
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, GetDealParticipantsChangelogOkResponseAdditionalData
            )
