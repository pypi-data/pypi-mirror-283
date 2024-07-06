from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class UpdateUserRequest(BaseModel):
    """UpdateUserRequest

    :param active_flag: Whether the user is active or not. `false` = Not activated, `true` = Activated
    :type active_flag: bool
    """

    def __init__(self, active_flag: bool):
        self.active_flag = active_flag
