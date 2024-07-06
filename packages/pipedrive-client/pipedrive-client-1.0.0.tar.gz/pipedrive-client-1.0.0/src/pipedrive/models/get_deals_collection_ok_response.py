from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class GetDealsCollectionOkResponseData(BaseModel):
    """GetDealsCollectionOkResponseData

    :param id_: The ID of the deal, defaults to None
    :type id_: int, optional
    :param creator_user_id: The ID of the deal creator, defaults to None
    :type creator_user_id: int, optional
    :param user_id: The ID of the user, defaults to None
    :type user_id: int, optional
    :param person_id: The ID of the person associated with the deal, defaults to None
    :type person_id: int, optional
    :param org_id: The ID of the organization associated with the deal, defaults to None
    :type org_id: int, optional
    :param stage_id: The ID of the deal stage, defaults to None
    :type stage_id: int, optional
    :param title: The title of the deal, defaults to None
    :type title: str, optional
    :param value: The value of the deal, defaults to None
    :type value: float, optional
    :param currency: The currency associated with the deal, defaults to None
    :type currency: str, optional
    :param add_time: The creation date and time of the deal in UTC. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type add_time: str, optional
    :param update_time: The last update date and time of the deal in UTC. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type update_time: str, optional
    :param status: The status of the deal, defaults to None
    :type status: str, optional
    :param probability: The success probability percentage of the deal, defaults to None
    :type probability: float, optional
    :param lost_reason: The reason for losing the deal, defaults to None
    :type lost_reason: str, optional
    :param visible_to: The visibility of the deal, defaults to None
    :type visible_to: str, optional
    :param close_time: The date and time of closing the deal in UTC. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type close_time: str, optional
    :param pipeline_id: The ID of the pipeline associated with the deal, defaults to None
    :type pipeline_id: int, optional
    :param won_time: The date and time of changing the deal status to won in UTC. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type won_time: str, optional
    :param lost_time: The date and time of changing the deal status to lost in UTC. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type lost_time: str, optional
    :param expected_close_date: The expected close date of the deal, defaults to None
    :type expected_close_date: str, optional
    :param label: The label or multiple labels assigned to the deal, defaults to None
    :type label: str, optional
    """

    def __init__(
        self,
        id_: int = None,
        creator_user_id: int = None,
        user_id: int = None,
        person_id: int = None,
        org_id: int = None,
        stage_id: int = None,
        title: str = None,
        value: float = None,
        currency: str = None,
        add_time: str = None,
        update_time: str = None,
        status: str = None,
        probability: float = None,
        lost_reason: str = None,
        visible_to: str = None,
        close_time: str = None,
        pipeline_id: int = None,
        won_time: str = None,
        lost_time: str = None,
        expected_close_date: str = None,
        label: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if creator_user_id is not None:
            self.creator_user_id = creator_user_id
        if user_id is not None:
            self.user_id = user_id
        if person_id is not None:
            self.person_id = person_id
        if org_id is not None:
            self.org_id = org_id
        if stage_id is not None:
            self.stage_id = stage_id
        if title is not None:
            self.title = title
        if value is not None:
            self.value = value
        if currency is not None:
            self.currency = currency
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time
        if status is not None:
            self.status = status
        if probability is not None:
            self.probability = probability
        if lost_reason is not None:
            self.lost_reason = lost_reason
        if visible_to is not None:
            self.visible_to = visible_to
        if close_time is not None:
            self.close_time = close_time
        if pipeline_id is not None:
            self.pipeline_id = pipeline_id
        if won_time is not None:
            self.won_time = won_time
        if lost_time is not None:
            self.lost_time = lost_time
        if expected_close_date is not None:
            self.expected_close_date = expected_close_date
        if label is not None:
            self.label = label


@JsonMap({})
class GetDealsCollectionOkResponseAdditionalData(BaseModel):
    """The additional data of the list

    :param next_cursor: The first item on the next page. The value of the `next_cursor` field will be `null` if you have reached the end of the dataset and there’s no more pages to be returned., defaults to None
    :type next_cursor: str, optional
    """

    def __init__(self, next_cursor: str = None):
        if next_cursor is not None:
            self.next_cursor = next_cursor


@JsonMap({})
class GetDealsCollectionOkResponse(BaseModel):
    """GetDealsCollectionOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: List[GetDealsCollectionOkResponseData], optional
    :param additional_data: The additional data of the list, defaults to None
    :type additional_data: GetDealsCollectionOkResponseAdditionalData, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: List[GetDealsCollectionOkResponseData] = None,
        additional_data: GetDealsCollectionOkResponseAdditionalData = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(data, GetDealsCollectionOkResponseData)
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, GetDealsCollectionOkResponseAdditionalData
            )
