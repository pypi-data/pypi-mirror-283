from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class DeleteWebhookOkResponse(BaseModel):
    """DeleteWebhookOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param status: The status of the response, defaults to None
    :type status: str, optional
    """

    def __init__(self, success: bool = None, status: str = None):
        if success is not None:
            self.success = success
        if status is not None:
            self.status = status
