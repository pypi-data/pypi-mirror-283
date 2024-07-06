from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class DeleteConversationOkResponse(BaseModel):
    """DeleteConversationOkResponse

    :param success: success, defaults to None
    :type success: bool, optional
    """

    def __init__(self, success: bool = None):
        if success is not None:
            self.success = success
