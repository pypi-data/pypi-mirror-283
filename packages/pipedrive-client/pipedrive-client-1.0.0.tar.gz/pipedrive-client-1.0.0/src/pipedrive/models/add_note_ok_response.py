from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class DataDeal2(BaseModel):
    """The deal this note is attached to

    :param title: The title of the deal this note is attached to, defaults to None
    :type title: str, optional
    """

    def __init__(self, title: str = None):
        if title is not None:
            self.title = title


@JsonMap({})
class DataOrganization2(BaseModel):
    """The organization the note is attached to

    :param name: The name of the organization the note is attached to, defaults to None
    :type name: str, optional
    """

    def __init__(self, name: str = None):
        if name is not None:
            self.name = name


@JsonMap({})
class DataPerson2(BaseModel):
    """The person the note is attached to

    :param name: The name of the person the note is attached to, defaults to None
    :type name: str, optional
    """

    def __init__(self, name: str = None):
        if name is not None:
            self.name = name


@JsonMap({})
class DataUser2(BaseModel):
    """The user who created the note

    :param email: The email of the note creator, defaults to None
    :type email: str, optional
    :param icon_url: The URL of the note creator avatar picture, defaults to None
    :type icon_url: str, optional
    :param is_you: Whether the note is created by you or not, defaults to None
    :type is_you: bool, optional
    :param name: The name of the note creator, defaults to None
    :type name: str, optional
    """

    def __init__(
        self,
        email: str = None,
        icon_url: str = None,
        is_you: bool = None,
        name: str = None,
    ):
        if email is not None:
            self.email = email
        if icon_url is not None:
            self.icon_url = icon_url
        if is_you is not None:
            self.is_you = is_you
        if name is not None:
            self.name = name


@JsonMap({"id_": "id"})
class AddNoteOkResponseData(BaseModel):
    """AddNoteOkResponseData

    :param id_: The ID of the note, defaults to None
    :type id_: int, optional
    :param active_flag: Whether the note is active or deleted, defaults to None
    :type active_flag: bool, optional
    :param add_time: The creation date and time of the note, defaults to None
    :type add_time: str, optional
    :param content: The content of the note in HTML format. Subject to sanitization on the back-end., defaults to None
    :type content: str, optional
    :param deal: The deal this note is attached to, defaults to None
    :type deal: DataDeal2, optional
    :param lead_id: The ID of the lead the note is attached to, defaults to None
    :type lead_id: str, optional
    :param deal_id: The ID of the deal the note is attached to, defaults to None
    :type deal_id: int, optional
    :param last_update_user_id: The ID of the user who last updated the note, defaults to None
    :type last_update_user_id: int, optional
    :param org_id: The ID of the organization the note is attached to, defaults to None
    :type org_id: int, optional
    :param organization: The organization the note is attached to, defaults to None
    :type organization: DataOrganization2, optional
    :param person: The person the note is attached to, defaults to None
    :type person: DataPerson2, optional
    :param person_id: The ID of the person the note is attached to, defaults to None
    :type person_id: int, optional
    :param pinned_to_deal_flag: If true, the results are filtered by note to deal pinning state, defaults to None
    :type pinned_to_deal_flag: bool, optional
    :param pinned_to_organization_flag: If true, the results are filtered by note to organization pinning state, defaults to None
    :type pinned_to_organization_flag: bool, optional
    :param pinned_to_person_flag: If true, the results are filtered by note to person pinning state, defaults to None
    :type pinned_to_person_flag: bool, optional
    :param update_time: The last updated date and time of the note, defaults to None
    :type update_time: str, optional
    :param user: The user who created the note, defaults to None
    :type user: DataUser2, optional
    :param user_id: The ID of the note creator, defaults to None
    :type user_id: int, optional
    """

    def __init__(
        self,
        id_: int = None,
        active_flag: bool = None,
        add_time: str = None,
        content: str = None,
        deal: DataDeal2 = None,
        lead_id: str = None,
        deal_id: int = None,
        last_update_user_id: int = None,
        org_id: int = None,
        organization: DataOrganization2 = None,
        person: DataPerson2 = None,
        person_id: int = None,
        pinned_to_deal_flag: bool = None,
        pinned_to_organization_flag: bool = None,
        pinned_to_person_flag: bool = None,
        update_time: str = None,
        user: DataUser2 = None,
        user_id: int = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if active_flag is not None:
            self.active_flag = active_flag
        if add_time is not None:
            self.add_time = add_time
        if content is not None:
            self.content = content
        if deal is not None:
            self.deal = self._define_object(deal, DataDeal2)
        if lead_id is not None:
            self.lead_id = lead_id
        if deal_id is not None:
            self.deal_id = deal_id
        if last_update_user_id is not None:
            self.last_update_user_id = last_update_user_id
        if org_id is not None:
            self.org_id = org_id
        if organization is not None:
            self.organization = self._define_object(organization, DataOrganization2)
        if person is not None:
            self.person = self._define_object(person, DataPerson2)
        if person_id is not None:
            self.person_id = person_id
        if pinned_to_deal_flag is not None:
            self.pinned_to_deal_flag = pinned_to_deal_flag
        if pinned_to_organization_flag is not None:
            self.pinned_to_organization_flag = pinned_to_organization_flag
        if pinned_to_person_flag is not None:
            self.pinned_to_person_flag = pinned_to_person_flag
        if update_time is not None:
            self.update_time = update_time
        if user is not None:
            self.user = self._define_object(user, DataUser2)
        if user_id is not None:
            self.user_id = user_id


@JsonMap({})
class AddNoteOkResponse(BaseModel):
    """AddNoteOkResponse

    :param success: If the request was successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: AddNoteOkResponseData, optional
    """

    def __init__(self, success: bool = None, data: AddNoteOkResponseData = None):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, AddNoteOkResponseData)
