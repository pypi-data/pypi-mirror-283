from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class GetUserConnectionsOkResponseData(BaseModel):
    """The object of UserConnections

    :param google: The third party ID or false in case the ID is not found, defaults to None
    :type google: str, optional
    """

    def __init__(self, google: str = None):
        if google is not None:
            self.google = google


@JsonMap({})
class GetUserConnectionsOkResponse(BaseModel):
    """GetUserConnectionsOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: The object of UserConnections, defaults to None
    :type data: GetUserConnectionsOkResponseData, optional
    """

    def __init__(
        self, success: bool = None, data: GetUserConnectionsOkResponseData = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, GetUserConnectionsOkResponseData)
