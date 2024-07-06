from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class SaveUserProviderLinkOkResponseData(BaseModel):
    """SaveUserProviderLinkOkResponseData

    :param message: The success message of the request, defaults to None
    :type message: str, optional
    """

    def __init__(self, message: str = None):
        if message is not None:
            self.message = message


@JsonMap({})
class SaveUserProviderLinkOkResponse(BaseModel):
    """SaveUserProviderLinkOkResponse

    :param success: Boolean that indicates whether the request was successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: SaveUserProviderLinkOkResponseData, optional
    """

    def __init__(
        self, success: bool = None, data: SaveUserProviderLinkOkResponseData = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, SaveUserProviderLinkOkResponseData)
