from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class UpdateCommentForNoteOkResponseData(BaseModel):
    """UpdateCommentForNoteOkResponseData

    :param uuid: The ID of the note, defaults to None
    :type uuid: str, optional
    :param active_flag: Whether the note is active or deleted, defaults to None
    :type active_flag: bool, optional
    :param add_time: The creation date and time of the note, defaults to None
    :type add_time: str, optional
    :param update_time: The creation date and time of the note, defaults to None
    :type update_time: str, optional
    :param content: The content of the note in HTML format. Subject to sanitization on the back-end., defaults to None
    :type content: str, optional
    :param object_id: The ID of the object that the comment is attached to, will be the id of the note, defaults to None
    :type object_id: str, optional
    :param object_type: The type of object that the comment is attached to, will be "note", defaults to None
    :type object_type: str, optional
    :param user_id: The ID of the user who created the comment, defaults to None
    :type user_id: int, optional
    :param updater_id: The ID of the user who last updated the comment, defaults to None
    :type updater_id: int, optional
    :param company_id: The ID of the company, defaults to None
    :type company_id: int, optional
    """

    def __init__(
        self,
        uuid: str = None,
        active_flag: bool = None,
        add_time: str = None,
        update_time: str = None,
        content: str = None,
        object_id: str = None,
        object_type: str = None,
        user_id: int = None,
        updater_id: int = None,
        company_id: int = None,
    ):
        if uuid is not None:
            self.uuid = uuid
        if active_flag is not None:
            self.active_flag = active_flag
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time
        if content is not None:
            self.content = content
        if object_id is not None:
            self.object_id = object_id
        if object_type is not None:
            self.object_type = object_type
        if user_id is not None:
            self.user_id = user_id
        if updater_id is not None:
            self.updater_id = updater_id
        if company_id is not None:
            self.company_id = company_id


@JsonMap({})
class UpdateCommentForNoteOkResponse(BaseModel):
    """UpdateCommentForNoteOkResponse

    :param success: If the request was successful or not, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: UpdateCommentForNoteOkResponseData, optional
    """

    def __init__(
        self, success: bool = None, data: UpdateCommentForNoteOkResponseData = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, UpdateCommentForNoteOkResponseData)
