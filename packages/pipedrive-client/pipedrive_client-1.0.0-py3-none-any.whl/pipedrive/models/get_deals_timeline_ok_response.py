from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class Deals(BaseModel):
    """Deals

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
class Totals(BaseModel):
    """The total values of deals for the given period

    :param count: The number of deals for the given period, defaults to None
    :type count: int, optional
    :param values: The total values of deals grouped by deal currency, defaults to None
    :type values: dict, optional
    :param weighted_values: The total weighted values of deals for the given period grouped by deal currency. The weighted value of a deal is calculated as probability times deal value., defaults to None
    :type weighted_values: dict, optional
    :param open_count: The number of open deals for the given period, defaults to None
    :type open_count: int, optional
    :param open_values: The total values of open deals for the given period grouped by deal currency, defaults to None
    :type open_values: dict, optional
    :param weighted_open_values: The total weighted values of open deals for the given period grouped by deal currency. The weighted value of a deal is calculated as probability times deal value., defaults to None
    :type weighted_open_values: dict, optional
    :param won_count: The number of won deals for the given period, defaults to None
    :type won_count: int, optional
    :param won_values: The total values of won deals for the given period grouped by deal currency, defaults to None
    :type won_values: dict, optional
    """

    def __init__(
        self,
        count: int = None,
        values: dict = None,
        weighted_values: dict = None,
        open_count: int = None,
        open_values: dict = None,
        weighted_open_values: dict = None,
        won_count: int = None,
        won_values: dict = None,
    ):
        if count is not None:
            self.count = count
        if values is not None:
            self.values = values
        if weighted_values is not None:
            self.weighted_values = weighted_values
        if open_count is not None:
            self.open_count = open_count
        if open_values is not None:
            self.open_values = open_values
        if weighted_open_values is not None:
            self.weighted_open_values = weighted_open_values
        if won_count is not None:
            self.won_count = won_count
        if won_values is not None:
            self.won_values = won_values


@JsonMap({})
class GetDealsTimelineOkResponseData(BaseModel):
    """Open and won deals grouped into periods by defined interval, amount and date-type dealField (`field_key`)

    :param period_start: The start date and time of the period, defaults to None
    :type period_start: str, optional
    :param period_end: The end date and time of the period, defaults to None
    :type period_end: str, optional
    :param deals: deals, defaults to None
    :type deals: List[Deals], optional
    :param totals: The total values of deals for the given period, defaults to None
    :type totals: Totals, optional
    """

    def __init__(
        self,
        period_start: str = None,
        period_end: str = None,
        deals: List[Deals] = None,
        totals: Totals = None,
    ):
        if period_start is not None:
            self.period_start = period_start
        if period_end is not None:
            self.period_end = period_end
        if deals is not None:
            self.deals = self._define_list(deals, Deals)
        if totals is not None:
            self.totals = self._define_object(totals, Totals)


@JsonMap({})
class GetDealsTimelineOkResponse(BaseModel):
    """GetDealsTimelineOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: Open and won deals grouped into periods by defined interval, amount and date-type dealField (`field_key`), defaults to None
    :type data: GetDealsTimelineOkResponseData, optional
    """

    def __init__(
        self, success: bool = None, data: GetDealsTimelineOkResponseData = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, GetDealsTimelineOkResponseData)
