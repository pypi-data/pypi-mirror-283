from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class DataCreatorUserId6(BaseModel):
    """The creator of the deal

    :param id_: The ID of the deal creator, defaults to None
    :type id_: int, optional
    :param name: The name of the deal creator, defaults to None
    :type name: str, optional
    :param email: The email of the deal creator, defaults to None
    :type email: str, optional
    :param has_pic: If the creator has a picture or not, defaults to None
    :type has_pic: bool, optional
    :param pic_hash: The creator picture hash, defaults to None
    :type pic_hash: str, optional
    :param active_flag: Whether the creator is active or not, defaults to None
    :type active_flag: bool, optional
    :param value: The ID of the deal creator, defaults to None
    :type value: int, optional
    """

    def __init__(
        self,
        id_: int = None,
        name: str = None,
        email: str = None,
        has_pic: bool = None,
        pic_hash: str = None,
        active_flag: bool = None,
        value: int = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        if has_pic is not None:
            self.has_pic = has_pic
        if pic_hash is not None:
            self.pic_hash = pic_hash
        if active_flag is not None:
            self.active_flag = active_flag
        if value is not None:
            self.value = value


@JsonMap({"id_": "id"})
class DataUserId6(BaseModel):
    """DataUserId6

    :param id_: The ID of the user, defaults to None
    :type id_: int, optional
    :param name: The name of the user, defaults to None
    :type name: str, optional
    :param email: The email of the user, defaults to None
    :type email: str, optional
    :param has_pic: If the user has a picture or not, defaults to None
    :type has_pic: bool, optional
    :param pic_hash: The user picture hash, defaults to None
    :type pic_hash: str, optional
    :param active_flag: Whether the user is active or not, defaults to None
    :type active_flag: bool, optional
    :param value: The ID of the user, defaults to None
    :type value: int, optional
    """

    def __init__(
        self,
        id_: int = None,
        name: str = None,
        email: str = None,
        has_pic: bool = None,
        pic_hash: str = None,
        active_flag: bool = None,
        value: int = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        if has_pic is not None:
            self.has_pic = has_pic
        if pic_hash is not None:
            self.pic_hash = pic_hash
        if active_flag is not None:
            self.active_flag = active_flag
        if value is not None:
            self.value = value


@JsonMap({})
class PersonIdEmail19(BaseModel):
    """PersonIdEmail19

    :param label: The type of the email, defaults to None
    :type label: str, optional
    :param value: The email of the associated person, defaults to None
    :type value: str, optional
    :param primary: If this is the primary email or not, defaults to None
    :type primary: bool, optional
    """

    def __init__(self, label: str = None, value: str = None, primary: bool = None):
        if label is not None:
            self.label = label
        if value is not None:
            self.value = value
        if primary is not None:
            self.primary = primary


@JsonMap({})
class PersonIdPhone19(BaseModel):
    """PersonIdPhone19

    :param label: The type of the phone number, defaults to None
    :type label: str, optional
    :param value: The phone number of the person associated with the deal, defaults to None
    :type value: str, optional
    :param primary: If this is the primary phone number or not, defaults to None
    :type primary: bool, optional
    """

    def __init__(self, label: str = None, value: str = None, primary: bool = None):
        if label is not None:
            self.label = label
        if value is not None:
            self.value = value
        if primary is not None:
            self.primary = primary


@JsonMap({})
class DataPersonId6(BaseModel):
    """DataPersonId6

    :param active_flag: Whether the associated person is active or not, defaults to None
    :type active_flag: bool, optional
    :param name: The name of the person associated with the deal, defaults to None
    :type name: str, optional
    :param email: The emails of the person associated with the deal, defaults to None
    :type email: List[PersonIdEmail19], optional
    :param phone: The phone numbers of the person associated with the deal, defaults to None
    :type phone: List[PersonIdPhone19], optional
    :param owner_id: The ID of the owner of the person that is associated with the deal, defaults to None
    :type owner_id: int, optional
    :param value: The ID of the person associated with the deal, defaults to None
    :type value: int, optional
    """

    def __init__(
        self,
        active_flag: bool = None,
        name: str = None,
        email: List[PersonIdEmail19] = None,
        phone: List[PersonIdPhone19] = None,
        owner_id: int = None,
        value: int = None,
    ):
        if active_flag is not None:
            self.active_flag = active_flag
        if name is not None:
            self.name = name
        if email is not None:
            self.email = self._define_list(email, PersonIdEmail19)
        if phone is not None:
            self.phone = self._define_list(phone, PersonIdPhone19)
        if owner_id is not None:
            self.owner_id = owner_id
        if value is not None:
            self.value = value


@JsonMap({})
class DataOrgId14(BaseModel):
    """DataOrgId14

    :param name: The name of the organization associated with the deal, defaults to None
    :type name: str, optional
    :param people_count: The number of people connected with the organization that is associated with the deal, defaults to None
    :type people_count: int, optional
    :param owner_id: The ID of the owner of the organization that is associated with the deal, defaults to None
    :type owner_id: int, optional
    :param address: The address of the organization that is associated with the deal, defaults to None
    :type address: str, optional
    :param active_flag: Whether the associated organization is active or not, defaults to None
    :type active_flag: bool, optional
    :param cc_email: The BCC email of the organization associated with the deal, defaults to None
    :type cc_email: str, optional
    :param value: The ID of the organization associated with the deal, defaults to None
    :type value: int, optional
    """

    def __init__(
        self,
        name: str = None,
        people_count: int = None,
        owner_id: int = None,
        address: str = None,
        active_flag: bool = None,
        cc_email: str = None,
        value: int = None,
    ):
        if name is not None:
            self.name = name
        if people_count is not None:
            self.people_count = people_count
        if owner_id is not None:
            self.owner_id = owner_id
        if address is not None:
            self.address = address
        if active_flag is not None:
            self.active_flag = active_flag
        if cc_email is not None:
            self.cc_email = cc_email
        if value is not None:
            self.value = value


@JsonMap({"id_": "id"})
class GetPersonDealsOkResponseData(BaseModel):
    """GetPersonDealsOkResponseData

    :param id_: The ID of the deal, defaults to None
    :type id_: int, optional
    :param creator_user_id: The creator of the deal, defaults to None
    :type creator_user_id: DataCreatorUserId6, optional
    :param user_id: user_id, defaults to None
    :type user_id: DataUserId6, optional
    :param person_id: person_id, defaults to None
    :type person_id: DataPersonId6, optional
    :param org_id: org_id, defaults to None
    :type org_id: DataOrgId14, optional
    :param stage_id: The ID of the deal stage, defaults to None
    :type stage_id: int, optional
    :param title: The title of the deal, defaults to None
    :type title: str, optional
    :param value: The value of the deal, defaults to None
    :type value: float, optional
    :param currency: The currency associated with the deal, defaults to None
    :type currency: str, optional
    :param add_time: The creation date and time of the deal, defaults to None
    :type add_time: str, optional
    :param update_time: The last updated date and time of the deal, defaults to None
    :type update_time: str, optional
    :param stage_change_time: The last updated date and time of the deal stage, defaults to None
    :type stage_change_time: str, optional
    :param active: Whether the deal is active or not, defaults to None
    :type active: bool, optional
    :param deleted: Whether the deal is deleted or not, defaults to None
    :type deleted: bool, optional
    :param status: The status of the deal, defaults to None
    :type status: str, optional
    :param probability: The success probability percentage of the deal, defaults to None
    :type probability: float, optional
    :param next_activity_date: The date of the next activity associated with the deal, defaults to None
    :type next_activity_date: str, optional
    :param next_activity_time: The time of the next activity associated with the deal, defaults to None
    :type next_activity_time: str, optional
    :param next_activity_id: The ID of the next activity associated with the deal, defaults to None
    :type next_activity_id: int, optional
    :param last_activity_id: The ID of the last activity associated with the deal, defaults to None
    :type last_activity_id: int, optional
    :param last_activity_date: The date of the last activity associated with the deal, defaults to None
    :type last_activity_date: str, optional
    :param lost_reason: The reason for losing the deal, defaults to None
    :type lost_reason: str, optional
    :param visible_to: The visibility of the deal, defaults to None
    :type visible_to: str, optional
    :param close_time: The date and time of closing the deal, defaults to None
    :type close_time: str, optional
    :param pipeline_id: The ID of the pipeline associated with the deal, defaults to None
    :type pipeline_id: int, optional
    :param won_time: The date and time of changing the deal status as won, defaults to None
    :type won_time: str, optional
    :param first_won_time: The date and time of the first time changing the deal status as won, defaults to None
    :type first_won_time: str, optional
    :param lost_time: The date and time of changing the deal status as lost, defaults to None
    :type lost_time: str, optional
    :param products_count: The number of products associated with the deal, defaults to None
    :type products_count: int, optional
    :param files_count: The number of files associated with the deal, defaults to None
    :type files_count: int, optional
    :param notes_count: The number of notes associated with the deal, defaults to None
    :type notes_count: int, optional
    :param followers_count: The number of followers associated with the deal, defaults to None
    :type followers_count: int, optional
    :param email_messages_count: The number of emails associated with the deal, defaults to None
    :type email_messages_count: int, optional
    :param activities_count: The number of activities associated with the deal, defaults to None
    :type activities_count: int, optional
    :param done_activities_count: The number of completed activities associated with the deal, defaults to None
    :type done_activities_count: int, optional
    :param undone_activities_count: The number of incomplete activities associated with the deal, defaults to None
    :type undone_activities_count: int, optional
    :param participants_count: The number of participants associated with the deal, defaults to None
    :type participants_count: int, optional
    :param expected_close_date: The expected close date of the deal, defaults to None
    :type expected_close_date: str, optional
    :param last_incoming_mail_time: The date and time of the last incoming email associated with the deal, defaults to None
    :type last_incoming_mail_time: str, optional
    :param last_outgoing_mail_time: The date and time of the last outgoing email associated with the deal, defaults to None
    :type last_outgoing_mail_time: str, optional
    :param label: The label or multiple labels assigned to the deal, defaults to None
    :type label: str, optional
    :param stage_order_nr: The order number of the deal stage associated with the deal, defaults to None
    :type stage_order_nr: int, optional
    :param person_name: The name of the person associated with the deal, defaults to None
    :type person_name: str, optional
    :param org_name: The name of the organization associated with the deal, defaults to None
    :type org_name: str, optional
    :param next_activity_subject: The subject of the next activity associated with the deal, defaults to None
    :type next_activity_subject: str, optional
    :param next_activity_type: The type of the next activity associated with the deal, defaults to None
    :type next_activity_type: str, optional
    :param next_activity_duration: The duration of the next activity associated with the deal, defaults to None
    :type next_activity_duration: str, optional
    :param next_activity_note: The note of the next activity associated with the deal, defaults to None
    :type next_activity_note: str, optional
    :param formatted_value: The deal value formatted with selected currency. E.g. US$500, defaults to None
    :type formatted_value: str, optional
    :param weighted_value: Probability times deal value. Probability can either be deal probability or if not set, then stage probability., defaults to None
    :type weighted_value: float, optional
    :param formatted_weighted_value: The weighted_value formatted with selected currency. E.g. US$500, defaults to None
    :type formatted_weighted_value: str, optional
    :param weighted_value_currency: The currency associated with the deal, defaults to None
    :type weighted_value_currency: str, optional
    :param rotten_time: The date and time of changing the deal status as rotten, defaults to None
    :type rotten_time: str, optional
    :param owner_name: The name of the deal owner, defaults to None
    :type owner_name: str, optional
    :param cc_email: The BCC email of the deal, defaults to None
    :type cc_email: str, optional
    :param org_hidden: If the organization that is associated with the deal is hidden or not, defaults to None
    :type org_hidden: bool, optional
    :param person_hidden: If the person that is associated with the deal is hidden or not, defaults to None
    :type person_hidden: bool, optional
    :param origin: The way this Deal was created. `origin` field is set by Pipedrive when Deal is created and cannot be changed., defaults to None
    :type origin: str, optional
    :param origin_id: The optional ID to further distinguish the origin of the deal - e.g. Which API integration created this Deal., defaults to None
    :type origin_id: str, optional
    :param channel: The ID of your Marketing channel this Deal was created from. Recognized Marketing channels can be configured in your <a href="https://app.pipedrive.com/settings/fields" target="_blank" rel="noopener noreferrer">Company settings</a>., defaults to None
    :type channel: int, optional
    :param channel_id: The optional ID to further distinguish the Marketing channel., defaults to None
    :type channel_id: str, optional
    :param arr: Only available in Advanced and above plans The Annual Recurring Revenue of the deal Null if there are no products attached to the deal , defaults to None
    :type arr: float, optional
    :param mrr: Only available in Advanced and above plans The Monthly Recurring Revenue of the deal Null if there are no products attached to the deal , defaults to None
    :type mrr: float, optional
    :param acv: Only available in Advanced and above plans The Annual Contract Value of the deal Null if there are no products attached to the deal , defaults to None
    :type acv: float, optional
    :param arr_currency: Only available in Advanced and above plans The Currency for Annual Recurring Revenue of the deal If the `arr` is null, this will also be null , defaults to None
    :type arr_currency: str, optional
    :param mrr_currency: Only available in Advanced and above plans The Currency for Monthly Recurring Revenue of the deal If the `mrr` is null, this will also be null , defaults to None
    :type mrr_currency: str, optional
    :param acv_currency: Only available in Advanced and above plans The Currency for Annual Contract Value of the deal If the `acv` is null, this will also be null , defaults to None
    :type acv_currency: str, optional
    """

    def __init__(
        self,
        id_: int = None,
        creator_user_id: DataCreatorUserId6 = None,
        user_id: DataUserId6 = None,
        person_id: DataPersonId6 = None,
        org_id: DataOrgId14 = None,
        stage_id: int = None,
        title: str = None,
        value: float = None,
        currency: str = None,
        add_time: str = None,
        update_time: str = None,
        stage_change_time: str = None,
        active: bool = None,
        deleted: bool = None,
        status: str = None,
        probability: float = None,
        next_activity_date: str = None,
        next_activity_time: str = None,
        next_activity_id: int = None,
        last_activity_id: int = None,
        last_activity_date: str = None,
        lost_reason: str = None,
        visible_to: str = None,
        close_time: str = None,
        pipeline_id: int = None,
        won_time: str = None,
        first_won_time: str = None,
        lost_time: str = None,
        products_count: int = None,
        files_count: int = None,
        notes_count: int = None,
        followers_count: int = None,
        email_messages_count: int = None,
        activities_count: int = None,
        done_activities_count: int = None,
        undone_activities_count: int = None,
        participants_count: int = None,
        expected_close_date: str = None,
        last_incoming_mail_time: str = None,
        last_outgoing_mail_time: str = None,
        label: str = None,
        stage_order_nr: int = None,
        person_name: str = None,
        org_name: str = None,
        next_activity_subject: str = None,
        next_activity_type: str = None,
        next_activity_duration: str = None,
        next_activity_note: str = None,
        formatted_value: str = None,
        weighted_value: float = None,
        formatted_weighted_value: str = None,
        weighted_value_currency: str = None,
        rotten_time: str = None,
        owner_name: str = None,
        cc_email: str = None,
        org_hidden: bool = None,
        person_hidden: bool = None,
        origin: str = None,
        origin_id: str = None,
        channel: int = None,
        channel_id: str = None,
        arr: float = None,
        mrr: float = None,
        acv: float = None,
        arr_currency: str = None,
        mrr_currency: str = None,
        acv_currency: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if creator_user_id is not None:
            self.creator_user_id = self._define_object(
                creator_user_id, DataCreatorUserId6
            )
        if user_id is not None:
            self.user_id = self._define_object(user_id, DataUserId6)
        if person_id is not None:
            self.person_id = self._define_object(person_id, DataPersonId6)
        if org_id is not None:
            self.org_id = self._define_object(org_id, DataOrgId14)
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
        if stage_change_time is not None:
            self.stage_change_time = stage_change_time
        if active is not None:
            self.active = active
        if deleted is not None:
            self.deleted = deleted
        if status is not None:
            self.status = status
        if probability is not None:
            self.probability = probability
        if next_activity_date is not None:
            self.next_activity_date = next_activity_date
        if next_activity_time is not None:
            self.next_activity_time = next_activity_time
        if next_activity_id is not None:
            self.next_activity_id = next_activity_id
        if last_activity_id is not None:
            self.last_activity_id = last_activity_id
        if last_activity_date is not None:
            self.last_activity_date = last_activity_date
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
        if first_won_time is not None:
            self.first_won_time = first_won_time
        if lost_time is not None:
            self.lost_time = lost_time
        if products_count is not None:
            self.products_count = products_count
        if files_count is not None:
            self.files_count = files_count
        if notes_count is not None:
            self.notes_count = notes_count
        if followers_count is not None:
            self.followers_count = followers_count
        if email_messages_count is not None:
            self.email_messages_count = email_messages_count
        if activities_count is not None:
            self.activities_count = activities_count
        if done_activities_count is not None:
            self.done_activities_count = done_activities_count
        if undone_activities_count is not None:
            self.undone_activities_count = undone_activities_count
        if participants_count is not None:
            self.participants_count = participants_count
        if expected_close_date is not None:
            self.expected_close_date = expected_close_date
        if last_incoming_mail_time is not None:
            self.last_incoming_mail_time = last_incoming_mail_time
        if last_outgoing_mail_time is not None:
            self.last_outgoing_mail_time = last_outgoing_mail_time
        if label is not None:
            self.label = label
        if stage_order_nr is not None:
            self.stage_order_nr = stage_order_nr
        if person_name is not None:
            self.person_name = person_name
        if org_name is not None:
            self.org_name = org_name
        if next_activity_subject is not None:
            self.next_activity_subject = next_activity_subject
        if next_activity_type is not None:
            self.next_activity_type = next_activity_type
        if next_activity_duration is not None:
            self.next_activity_duration = next_activity_duration
        if next_activity_note is not None:
            self.next_activity_note = next_activity_note
        if formatted_value is not None:
            self.formatted_value = formatted_value
        if weighted_value is not None:
            self.weighted_value = weighted_value
        if formatted_weighted_value is not None:
            self.formatted_weighted_value = formatted_weighted_value
        if weighted_value_currency is not None:
            self.weighted_value_currency = weighted_value_currency
        if rotten_time is not None:
            self.rotten_time = rotten_time
        if owner_name is not None:
            self.owner_name = owner_name
        if cc_email is not None:
            self.cc_email = cc_email
        if org_hidden is not None:
            self.org_hidden = org_hidden
        if person_hidden is not None:
            self.person_hidden = person_hidden
        if origin is not None:
            self.origin = origin
        if origin_id is not None:
            self.origin_id = origin_id
        if channel is not None:
            self.channel = channel
        if channel_id is not None:
            self.channel_id = channel_id
        if arr is not None:
            self.arr = arr
        if mrr is not None:
            self.mrr = mrr
        if acv is not None:
            self.acv = acv
        if arr_currency is not None:
            self.arr_currency = arr_currency
        if mrr_currency is not None:
            self.mrr_currency = mrr_currency
        if acv_currency is not None:
            self.acv_currency = acv_currency


@JsonMap({})
class GetPersonDealsOkResponseAdditionalData(BaseModel):
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


@JsonMap({"id_": "id"})
class OrganizationOrganizationId26(BaseModel):
    """OrganizationOrganizationId26

    :param active_flag: Whether the associated organization is active or not, defaults to None
    :type active_flag: bool, optional
    :param id_: The ID of the organization associated with the item, defaults to None
    :type id_: int, optional
    :param name: The name of the organization associated with the item, defaults to None
    :type name: str, optional
    :param people_count: The number of people connected with the organization that is associated with the item, defaults to None
    :type people_count: int, optional
    :param owner_id: The ID of the owner of the organization that is associated with the item, defaults to None
    :type owner_id: int, optional
    :param address: The address of the organization, defaults to None
    :type address: str, optional
    :param cc_email: The BCC email of the organization associated with the item, defaults to None
    :type cc_email: str, optional
    """

    def __init__(
        self,
        active_flag: bool = None,
        id_: int = None,
        name: str = None,
        people_count: int = None,
        owner_id: int = None,
        address: str = None,
        cc_email: str = None,
    ):
        if active_flag is not None:
            self.active_flag = active_flag
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if people_count is not None:
            self.people_count = people_count
        if owner_id is not None:
            self.owner_id = owner_id
        if address is not None:
            self.address = address
        if cc_email is not None:
            self.cc_email = cc_email


@JsonMap({"organization_id": "ORGANIZATION_ID"})
class RelatedObjectsOrganization26(BaseModel):
    """RelatedObjectsOrganization26

    :param organization_id: organization_id, defaults to None
    :type organization_id: OrganizationOrganizationId26, optional
    """

    def __init__(self, organization_id: OrganizationOrganizationId26 = None):
        if organization_id is not None:
            self.organization_id = self._define_object(
                organization_id, OrganizationOrganizationId26
            )


@JsonMap({})
class PersonIdEmail20(BaseModel):
    """PersonIdEmail20

    :param label: The type of the email, defaults to None
    :type label: str, optional
    :param value: The email of the associated person, defaults to None
    :type value: str, optional
    :param primary: Whether this is the primary email or not, defaults to None
    :type primary: bool, optional
    """

    def __init__(self, label: str = None, value: str = None, primary: bool = None):
        if label is not None:
            self.label = label
        if value is not None:
            self.value = value
        if primary is not None:
            self.primary = primary


@JsonMap({})
class PersonIdPhone20(BaseModel):
    """PersonIdPhone20

    :param label: The type of the phone number, defaults to None
    :type label: str, optional
    :param value: The phone number of the person associated with the item, defaults to None
    :type value: str, optional
    :param primary: Whether this is the primary phone number or not, defaults to None
    :type primary: bool, optional
    """

    def __init__(self, label: str = None, value: str = None, primary: bool = None):
        if label is not None:
            self.label = label
        if value is not None:
            self.value = value
        if primary is not None:
            self.primary = primary


@JsonMap({"id_": "id"})
class PersonPersonId14(BaseModel):
    """PersonPersonId14

    :param active_flag: Whether the associated person is active or not, defaults to None
    :type active_flag: bool, optional
    :param id_: The ID of the person associated with the item, defaults to None
    :type id_: int, optional
    :param name: The name of the person associated with the item, defaults to None
    :type name: str, optional
    :param email: The emails of the person associated with the item, defaults to None
    :type email: List[PersonIdEmail20], optional
    :param phone: The phone numbers of the person associated with the item, defaults to None
    :type phone: List[PersonIdPhone20], optional
    :param owner_id: The ID of the owner of the person that is associated with the item, defaults to None
    :type owner_id: int, optional
    """

    def __init__(
        self,
        active_flag: bool = None,
        id_: int = None,
        name: str = None,
        email: List[PersonIdEmail20] = None,
        phone: List[PersonIdPhone20] = None,
        owner_id: int = None,
    ):
        if active_flag is not None:
            self.active_flag = active_flag
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if email is not None:
            self.email = self._define_list(email, PersonIdEmail20)
        if phone is not None:
            self.phone = self._define_list(phone, PersonIdPhone20)
        if owner_id is not None:
            self.owner_id = owner_id


@JsonMap({"person_id": "PERSON_ID"})
class RelatedObjectsPerson14(BaseModel):
    """RelatedObjectsPerson14

    :param person_id: person_id, defaults to None
    :type person_id: PersonPersonId14, optional
    """

    def __init__(self, person_id: PersonPersonId14 = None):
        if person_id is not None:
            self.person_id = self._define_object(person_id, PersonPersonId14)


@JsonMap({"id_": "id"})
class UserUserId26(BaseModel):
    """UserUserId26

    :param id_: The ID of the user, defaults to None
    :type id_: int, optional
    :param name: The name of the user, defaults to None
    :type name: str, optional
    :param email: The email of the user, defaults to None
    :type email: str, optional
    :param has_pic: Whether the user has picture or not. 0 = No picture, 1 = Has picture., defaults to None
    :type has_pic: int, optional
    :param pic_hash: The user picture hash, defaults to None
    :type pic_hash: str, optional
    :param active_flag: Whether the user is active or not, defaults to None
    :type active_flag: bool, optional
    """

    def __init__(
        self,
        id_: int = None,
        name: str = None,
        email: str = None,
        has_pic: int = None,
        pic_hash: str = None,
        active_flag: bool = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        if has_pic is not None:
            self.has_pic = has_pic
        if pic_hash is not None:
            self.pic_hash = pic_hash
        if active_flag is not None:
            self.active_flag = active_flag


@JsonMap({"user_id": "USER_ID"})
class RelatedObjectsUser26(BaseModel):
    """RelatedObjectsUser26

    :param user_id: user_id, defaults to None
    :type user_id: UserUserId26, optional
    """

    def __init__(self, user_id: UserUserId26 = None):
        if user_id is not None:
            self.user_id = self._define_object(user_id, UserUserId26)


@JsonMap({"id_": "id"})
class RelatedObjectsStage2(BaseModel):
    """RelatedObjectsStage2

    :param id_: The ID of the stage, defaults to None
    :type id_: int, optional
    :param order_nr: Defines the order of the stage, defaults to None
    :type order_nr: int, optional
    :param name: The name of the stage, defaults to None
    :type name: str, optional
    :param active_flag: Whether the stage is active or deleted, defaults to None
    :type active_flag: bool, optional
    :param deal_probability: The success probability percentage of the deal. Used/shown when the deal weighted values are used., defaults to None
    :type deal_probability: int, optional
    :param pipeline_id: The ID of the pipeline to add the stage to, defaults to None
    :type pipeline_id: int, optional
    :param rotten_flag: Whether deals in this stage can become rotten, defaults to None
    :type rotten_flag: bool, optional
    :param rotten_days: The number of days the deals not updated in this stage would become rotten. Applies only if the `rotten_flag` is set., defaults to None
    :type rotten_days: int, optional
    :param add_time: The stage creation time. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type add_time: str, optional
    :param update_time: The stage update time. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type update_time: str, optional
    """

    def __init__(
        self,
        id_: int = None,
        order_nr: int = None,
        name: str = None,
        active_flag: bool = None,
        deal_probability: int = None,
        pipeline_id: int = None,
        rotten_flag: bool = None,
        rotten_days: int = None,
        add_time: str = None,
        update_time: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if order_nr is not None:
            self.order_nr = order_nr
        if name is not None:
            self.name = name
        if active_flag is not None:
            self.active_flag = active_flag
        if deal_probability is not None:
            self.deal_probability = deal_probability
        if pipeline_id is not None:
            self.pipeline_id = pipeline_id
        if rotten_flag is not None:
            self.rotten_flag = rotten_flag
        if rotten_days is not None:
            self.rotten_days = rotten_days
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time


@JsonMap({"id_": "id"})
class RelatedObjectsPipeline2(BaseModel):
    """RelatedObjectsPipeline2

    :param id_: The ID of the pipeline, defaults to None
    :type id_: int, optional
    :param name: The name of the pipeline, defaults to None
    :type name: str, optional
    :param url_title: The pipeline title displayed in the URL, defaults to None
    :type url_title: str, optional
    :param order_nr: Defines the order of pipelines. First order (`order_nr=0`) is the default pipeline., defaults to None
    :type order_nr: int, optional
    :param active: Whether this pipeline will be made inactive (hidden) or active, defaults to None
    :type active: bool, optional
    :param deal_probability: Whether deal probability is disabled or enabled for this pipeline, defaults to None
    :type deal_probability: bool, optional
    :param add_time: The pipeline creation time. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type add_time: str, optional
    :param update_time: The pipeline update time. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type update_time: str, optional
    """

    def __init__(
        self,
        id_: int = None,
        name: str = None,
        url_title: str = None,
        order_nr: int = None,
        active: bool = None,
        deal_probability: bool = None,
        add_time: str = None,
        update_time: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if url_title is not None:
            self.url_title = url_title
        if order_nr is not None:
            self.order_nr = order_nr
        if active is not None:
            self.active = active
        if deal_probability is not None:
            self.deal_probability = deal_probability
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time


@JsonMap({})
class GetPersonDealsOkResponseRelatedObjects(BaseModel):
    """GetPersonDealsOkResponseRelatedObjects

    :param organization: organization, defaults to None
    :type organization: RelatedObjectsOrganization26, optional
    :param person: person, defaults to None
    :type person: RelatedObjectsPerson14, optional
    :param user: user, defaults to None
    :type user: RelatedObjectsUser26, optional
    :param stage: stage, defaults to None
    :type stage: RelatedObjectsStage2, optional
    :param pipeline: pipeline, defaults to None
    :type pipeline: RelatedObjectsPipeline2, optional
    """

    def __init__(
        self,
        organization: RelatedObjectsOrganization26 = None,
        person: RelatedObjectsPerson14 = None,
        user: RelatedObjectsUser26 = None,
        stage: RelatedObjectsStage2 = None,
        pipeline: RelatedObjectsPipeline2 = None,
    ):
        if organization is not None:
            self.organization = self._define_object(
                organization, RelatedObjectsOrganization26
            )
        if person is not None:
            self.person = self._define_object(person, RelatedObjectsPerson14)
        if user is not None:
            self.user = self._define_object(user, RelatedObjectsUser26)
        if stage is not None:
            self.stage = self._define_object(stage, RelatedObjectsStage2)
        if pipeline is not None:
            self.pipeline = self._define_object(pipeline, RelatedObjectsPipeline2)


@JsonMap({})
class GetPersonDealsOkResponse(BaseModel):
    """GetPersonDealsOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: The array of deals, defaults to None
    :type data: List[GetPersonDealsOkResponseData], optional
    :param additional_data: The additional data of the list, defaults to None
    :type additional_data: GetPersonDealsOkResponseAdditionalData, optional
    :param related_objects: related_objects, defaults to None
    :type related_objects: GetPersonDealsOkResponseRelatedObjects, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: List[GetPersonDealsOkResponseData] = None,
        additional_data: GetPersonDealsOkResponseAdditionalData = None,
        related_objects: GetPersonDealsOkResponseRelatedObjects = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(data, GetPersonDealsOkResponseData)
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, GetPersonDealsOkResponseAdditionalData
            )
        if related_objects is not None:
            self.related_objects = self._define_object(
                related_objects, GetPersonDealsOkResponseRelatedObjects
            )
