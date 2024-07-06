from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class DataEmail7(BaseModel):
    """DataEmail7

    :param value: The email, defaults to None
    :type value: str, optional
    :param primary: Boolean that indicates if email is primary for the person or not, defaults to None
    :type primary: bool, optional
    :param label: The label that indicates the type of the email. (Possible values - work, home or other), defaults to None
    :type label: str, optional
    """

    def __init__(self, value: str = None, primary: bool = None, label: str = None):
        if value is not None:
            self.value = value
        if primary is not None:
            self.primary = primary
        if label is not None:
            self.label = label


@JsonMap({})
class DataPhone7(BaseModel):
    """DataPhone7

    :param value: The phone number, defaults to None
    :type value: str, optional
    :param primary: Boolean that indicates if phone number is primary for the person or not, defaults to None
    :type primary: bool, optional
    :param label: The label that indicates the type of the phone number. (Possible values - work, home, mobile or other), defaults to None
    :type label: str, optional
    """

    def __init__(self, value: str = None, primary: bool = None, label: str = None):
        if value is not None:
            self.value = value
        if primary is not None:
            self.primary = primary
        if label is not None:
            self.label = label


@JsonMap({"id_": "id"})
class GetPersonsCollectionOkResponseData(BaseModel):
    """GetPersonsCollectionOkResponseData

    :param id_: The ID of the person, defaults to None
    :type id_: int, optional
    :param active_flag: Whether the person is active or not, defaults to None
    :type active_flag: bool, optional
    :param owner_id: The ID of the owner related to the person, defaults to None
    :type owner_id: int, optional
    :param org_id: The ID of the organization related to the person, defaults to None
    :type org_id: int, optional
    :param name: The name of the person, defaults to None
    :type name: str, optional
    :param email: An email address as a string or an array of email objects related to the person. The structure of the array is as follows: `[{ "value": "mail@example.com", "primary": "true", "label": "main" }]`. Please note that only `value` is required., defaults to None
    :type email: List[DataEmail7], optional
    :param phone: A phone number supplied as a string or an array of phone objects related to the person. The structure of the array is as follows: `[{ "value": "12345", "primary": "true", "label": "mobile" }]`. Please note that only `value` is required., defaults to None
    :type phone: List[DataPhone7], optional
    :param update_time: The last updated date and time of the person. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type update_time: str, optional
    :param delete_time: The date and time this person was deleted. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type delete_time: str, optional
    :param add_time: The date and time when the person was added/created. Format: YYYY-MM-DD HH:MM:SS, defaults to None
    :type add_time: str, optional
    :param visible_to: The visibility group ID of who can see the person, defaults to None
    :type visible_to: str, optional
    :param picture_id: The ID of the picture associated with the item, defaults to None
    :type picture_id: int, optional
    :param label: The label assigned to the person, defaults to None
    :type label: int, optional
    :param cc_email: The BCC email associated with the person, defaults to None
    :type cc_email: str, optional
    """

    def __init__(
        self,
        id_: int = None,
        active_flag: bool = None,
        owner_id: int = None,
        org_id: int = None,
        name: str = None,
        email: List[DataEmail7] = None,
        phone: List[DataPhone7] = None,
        update_time: str = None,
        delete_time: str = None,
        add_time: str = None,
        visible_to: str = None,
        picture_id: int = None,
        label: int = None,
        cc_email: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if active_flag is not None:
            self.active_flag = active_flag
        if owner_id is not None:
            self.owner_id = owner_id
        if org_id is not None:
            self.org_id = org_id
        if name is not None:
            self.name = name
        if email is not None:
            self.email = self._define_list(email, DataEmail7)
        if phone is not None:
            self.phone = self._define_list(phone, DataPhone7)
        if update_time is not None:
            self.update_time = update_time
        if delete_time is not None:
            self.delete_time = delete_time
        if add_time is not None:
            self.add_time = add_time
        if visible_to is not None:
            self.visible_to = visible_to
        if picture_id is not None:
            self.picture_id = picture_id
        if label is not None:
            self.label = label
        if cc_email is not None:
            self.cc_email = cc_email


@JsonMap({})
class GetPersonsCollectionOkResponseAdditionalData(BaseModel):
    """The additional data of the list

    :param next_cursor: The first item on the next page. The value of the `next_cursor` field will be `null` if you have reached the end of the dataset and there’s no more pages to be returned., defaults to None
    :type next_cursor: str, optional
    """

    def __init__(self, next_cursor: str = None):
        if next_cursor is not None:
            self.next_cursor = next_cursor


@JsonMap({})
class GetPersonsCollectionOkResponse(BaseModel):
    """GetPersonsCollectionOkResponse

    :param success: success, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: List[GetPersonsCollectionOkResponseData], optional
    :param additional_data: The additional data of the list, defaults to None
    :type additional_data: GetPersonsCollectionOkResponseAdditionalData, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: List[GetPersonsCollectionOkResponseData] = None,
        additional_data: GetPersonsCollectionOkResponseAdditionalData = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(data, GetPersonsCollectionOkResponseData)
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, GetPersonsCollectionOkResponseAdditionalData
            )
