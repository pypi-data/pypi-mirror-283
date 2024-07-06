from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


class DataDone1(Enum):
    """An enumeration representing different categories.

    :cvar _0: 0
    :vartype _0: str
    :cvar _1: 1
    :vartype _1: str
    """

    _0 = 0
    _1 = 1

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, DataDone1._member_map_.values()))


@JsonMap({"id_": "id"})
class GetProjectTasksOkResponseData(BaseModel):
    """GetProjectTasksOkResponseData

    :param id_: The ID of the task, generated when the task was created, defaults to None
    :type id_: int, optional
    :param title: The title of the task, defaults to None
    :type title: str, optional
    :param project_id: The ID of the project this task is associated with, defaults to None
    :type project_id: float, optional
    :param description: The description of the task, defaults to None
    :type description: str, optional
    :param parent_task_id: The ID of a parent task. Can not be ID of a task which is already a subtask., defaults to None
    :type parent_task_id: float, optional
    :param assignee_id: The ID of the user who will be the assignee of the task, defaults to None
    :type assignee_id: float, optional
    :param done: done, defaults to None
    :type done: DataDone1, optional
    :param due_date: The due date of the task. Format: YYYY-MM-DD., defaults to None
    :type due_date: str, optional
    :param creator_id: The creator of a task, defaults to None
    :type creator_id: float, optional
    :param add_time: The creation date and time of the task in UTC. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type add_time: str, optional
    :param update_time: The update date and time of the task in UTC. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type update_time: str, optional
    :param marked_as_done_time: The marked as done date and time of the task in UTC. Format: YYYY-MM-DD HH:MM:SS., defaults to None
    :type marked_as_done_time: str, optional
    """

    def __init__(
        self,
        id_: int = None,
        title: str = None,
        project_id: float = None,
        description: str = None,
        parent_task_id: float = None,
        assignee_id: float = None,
        done: DataDone1 = None,
        due_date: str = None,
        creator_id: float = None,
        add_time: str = None,
        update_time: str = None,
        marked_as_done_time: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if title is not None:
            self.title = title
        if project_id is not None:
            self.project_id = project_id
        if description is not None:
            self.description = description
        if parent_task_id is not None:
            self.parent_task_id = parent_task_id
        if assignee_id is not None:
            self.assignee_id = assignee_id
        if done is not None:
            self.done = self._enum_matching(done, DataDone1.list(), "done")
        if due_date is not None:
            self.due_date = due_date
        if creator_id is not None:
            self.creator_id = creator_id
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time
        if marked_as_done_time is not None:
            self.marked_as_done_time = marked_as_done_time


@JsonMap({})
class GetProjectTasksOkResponseAdditionalData(BaseModel):
    """The additional data of the list

    :param next_cursor: The first item on the next page. The value of the `next_cursor` field will be `null` if you have reached the end of the dataset and there’s no more pages to be returned., defaults to None
    :type next_cursor: str, optional
    """

    def __init__(self, next_cursor: str = None):
        if next_cursor is not None:
            self.next_cursor = next_cursor


@JsonMap({})
class GetProjectTasksOkResponse(BaseModel):
    """GetProjectTasksOkResponse

    :param success: success, defaults to None
    :type success: bool, optional
    :param data: data, defaults to None
    :type data: List[GetProjectTasksOkResponseData], optional
    :param additional_data: The additional data of the list, defaults to None
    :type additional_data: GetProjectTasksOkResponseAdditionalData, optional
    """

    def __init__(
        self,
        success: bool = None,
        data: List[GetProjectTasksOkResponseData] = None,
        additional_data: GetProjectTasksOkResponseAdditionalData = None,
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_list(data, GetProjectTasksOkResponseData)
        if additional_data is not None:
            self.additional_data = self._define_object(
                additional_data, GetProjectTasksOkResponseAdditionalData
            )
