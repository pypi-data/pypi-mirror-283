from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class GetCompanyAddonsOkResponse(BaseModel):
    """GetCompanyAddonsOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: An array of add-ons that the company has., defaults to None
    :type data: List[dict], optional
    """

    def __init__(self, success: bool = None, data: List[dict] = None):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = data
