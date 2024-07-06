from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class UpdateCommentForNoteRequest(BaseModel):
    """UpdateCommentForNoteRequest

    :param content: The content of the comment in HTML format. Subject to sanitization on the back-end.
    :type content: str
    """

    def __init__(self, content: str):
        self.content = content
