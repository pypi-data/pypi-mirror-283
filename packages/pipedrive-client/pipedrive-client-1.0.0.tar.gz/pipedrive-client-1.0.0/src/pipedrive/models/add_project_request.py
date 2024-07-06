from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class AddProjectRequest(BaseModel):
    """AddProjectRequest

    :param title: The title of the project
    :type title: str
    :param board_id: The ID of a project board
    :type board_id: float
    :param phase_id: The ID of a phase on a project board
    :type phase_id: float
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
    :param template_id: The ID of the template the project will be based on, defaults to None
    :type template_id: float, optional
    """

    def __init__(
        self,
        title: str,
        board_id: float,
        phase_id: float,
        description: str = None,
        status: str = None,
        owner_id: float = None,
        start_date: str = None,
        end_date: str = None,
        deal_ids: List[int] = None,
        org_id: float = None,
        person_id: float = None,
        labels: List[int] = None,
        template_id: float = None,
    ):
        self.title = title
        self.board_id = board_id
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
        if template_id is not None:
            self.template_id = template_id
