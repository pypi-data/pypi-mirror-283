from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class UpdateFileRequest(BaseModel):
    """UpdateFileRequest

    :param name: The visible name of the file, defaults to None
    :type name: str, optional
    :param description: The description of the file, defaults to None
    :type description: str, optional
    """

    def __init__(self, name: str = None, description: str = None):
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
