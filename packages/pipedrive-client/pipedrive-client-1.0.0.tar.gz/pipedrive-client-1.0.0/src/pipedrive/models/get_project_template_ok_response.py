from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"id_": "id"})
class GetProjectTemplateOkResponseData(BaseModel):
    """GetProjectTemplateOkResponseData

    :param id_: The ID of a template, defaults to None
    :type id_: float, optional
    :param title: The title of a template, defaults to None
    :type title: str, optional
    :param description: The description of a template, defaults to None
    :type description: str, optional
    :param projects_board_id: The ID of the project board this template is associated with, defaults to None
    :type projects_board_id: float, optional
    :param owner_id: The ID of a template owner, defaults to None
    :type owner_id: float, optional
    :param add_time: The creation date and time of the template in UTC. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type add_time: str, optional
    :param update_time: The update date and time of the template in UTC. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type update_time: str, optional
    """

    def __init__(
        self,
        id_: float = None,
        title: str = None,
        description: str = None,
        projects_board_id: float = None,
        owner_id: float = None,
        add_time: str = None,
        update_time: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if projects_board_id is not None:
            self.projects_board_id = projects_board_id
        if owner_id is not None:
            self.owner_id = owner_id
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time


@JsonMap({})
class GetProjectTemplateOkResponse(BaseModel):
    """GetProjectTemplateOkResponse

    :param success: success, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: GetProjectTemplateOkResponseData, optional
    :param additional_data: additional_data, defaults to None
    :type additional_data: dict, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: GetProjectTemplateOkResponseData = None,
        additional_data: dict = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, GetProjectTemplateOkResponseData)
        if additional_data is not None:
            self.additional_data = additional_data
