from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class AddCallLogAudioFileRequest(BaseModel):
    """AddCallLogAudioFileRequest

    :param file: Audio file supported by the HTML5 specification
    :type file: any
    """

    def __init__(self, file: any):
        self.file = file
