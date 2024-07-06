from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class GetProjectOkResponseData(BaseModel):
    """GetProjectOkResponseData

    :param id_: The ID of the project, generated when the task was created, defaults to None
    :type id_: int, optional
    :param title: The title of the project, defaults to None
    :type title: str, optional
    :param board_id: The ID of the board this project is associated with, defaults to None
    :type board_id: float, optional
    :param phase_id: The ID of the phase this project is associated with, defaults to None
    :type phase_id: float, optional
    :param description: The description of the project, defaults to None
    :type description: str, optional
    :param status: The status of the project, defaults to None
    :type status: str, optional
    :param owner_id: The ID of a project owner, defaults to None
    :type owner_id: float, optional
    :param start_date: The start date of the project. Format: YYYY-MM-DD., defaults to None
    :type start_date: str, optional
    :param end_date: The end date of the project. Format: YYYY-MM-DD., defaults to None
    :type end_date: str, optional
    :param deal_ids: An array of IDs of the deals this project is associated with, defaults to None
    :type deal_ids: List[int], optional
    :param org_id: The ID of the organization this project is associated with, defaults to None
    :type org_id: float, optional
    :param person_id: The ID of the person this project is associated with, defaults to None
    :type person_id: float, optional
    :param labels: An array of IDs of the labels this project has, defaults to None
    :type labels: List[int], optional
    :param add_time: The creation date and time of the project in UTC. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type add_time: str, optional
    :param update_time: The update date and time of the project in UTC. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type update_time: str, optional
    :param status_change_time: The status changed date and time of the project in UTC. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type status_change_time: str, optional
    :param archive_time: The archived date and time of the project in UTC. Format: YYYY-MM-DD HH:MM:SS. If not archived then 'null'., defaults to None
    :type archive_time: str, optional
    """

    def __init__(
        self,
        id_: int = None,
        title: str = None,
        board_id: float = None,
        phase_id: float = None,
        description: str = None,
        status: str = None,
        owner_id: float = None,
        start_date: str = None,
        end_date: str = None,
        deal_ids: List[int] = None,
        org_id: float = None,
        person_id: float = None,
        labels: List[int] = None,
        add_time: str = None,
        update_time: str = None,
        status_change_time: str = None,
        archive_time: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if title is not None:
            self.title = title
        if board_id is not None:
            self.board_id = board_id
        if phase_id is not None:
            self.phase_id = phase_id
        if description is not None:
            self.description = description
        if status is not None:
            self.status = status
        if owner_id is not None:
            self.owner_id = owner_id
        if start_date is not None:
            self.start_date = start_date
        if end_date is not None:
            self.end_date = end_date
        if deal_ids is not None:
            self.deal_ids = deal_ids
        if org_id is not None:
            self.org_id = org_id
        if person_id is not None:
            self.person_id = person_id
        if labels is not None:
            self.labels = labels
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time
        if status_change_time is not None:
            self.status_change_time = status_change_time
        if archive_time is not None:
            self.archive_time = archive_time


@JsonMap({})
class GetProjectOkResponse(BaseModel):
    """GetProjectOkResponse

    :param success: success, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: GetProjectOkResponseData, optional
    :param additional_data: additional_data, defaults to None
    :type additional_data: dict, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: GetProjectOkResponseData = None,
        additional_data: dict = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, GetProjectOkResponseData)
        if additional_data is not None:
            self.additional_data = additional_data
