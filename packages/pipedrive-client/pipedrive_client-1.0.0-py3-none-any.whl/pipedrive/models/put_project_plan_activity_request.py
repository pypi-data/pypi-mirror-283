from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class PutProjectPlanActivityRequest(BaseModel):
    """PutProjectPlanActivityRequest

    :param phase_id: The ID of a phase on a project board, defaults to None
    :type phase_id: float, optional
    :param group_id: The ID of a group on a project board, defaults to None
    :type group_id: float, optional
    """

    def __init__(self, phase_id: float = None, group_id: float = None):
        if phase_id is not None:
            self.phase_id = phase_id
        if group_id is not None:
            self.group_id = group_id
