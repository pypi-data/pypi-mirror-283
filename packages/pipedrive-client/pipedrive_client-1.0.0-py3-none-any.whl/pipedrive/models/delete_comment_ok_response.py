from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class DeleteCommentOkResponse(BaseModel):
    """DeleteCommentOkResponse

    :param success: If the request was successful or not, defaults to None
    :type success: bool, optional
    :param data: If the response is successful or not, defaults to None
    :type data: bool, optional
    """

    def __init__(self, success: bool = None, data: bool = None):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = data
