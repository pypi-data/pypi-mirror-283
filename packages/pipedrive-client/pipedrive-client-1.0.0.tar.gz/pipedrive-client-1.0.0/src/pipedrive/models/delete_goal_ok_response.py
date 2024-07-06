from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class DeleteGoalOkResponse(BaseModel):
    """DeleteGoalOkResponse

    :param success: If the request was successful or not, defaults to None
    :type success: bool, optional
    """

    def __init__(self, success: bool = None):
        if success is not None:
            self.success = success
