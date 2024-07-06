from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class AddTaskRequestDone(Enum):
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
        return list(map(lambda x: x.value, AddTaskRequestDone._member_map_.values()))


@JsonMap({})
class AddTaskRequest(BaseModel):
    """AddTaskRequest

    :param title: The title of the task
    :type title: str
    :param project_id: The ID of a project
    :type project_id: float
    :param description: The description of the task, defaults to None
    :type description: str, optional
    :param parent_task_id: The ID of a parent task. Can not be ID of a task which is already a subtask., defaults to None
    :type parent_task_id: float, optional
    :param assignee_id: The ID of the user who will be the assignee of the task, defaults to None
    :type assignee_id: float, optional
    :param done: done, defaults to None
    :type done: AddTaskRequestDone, optional
    :param due_date: The due date of the task. Format: YYYY-MM-DD., defaults to None
    :type due_date: str, optional
    """

    def __init__(
        self,
        title: str,
        project_id: float,
        description: str = None,
        parent_task_id: float = None,
        assignee_id: float = None,
        done: AddTaskRequestDone = None,
        due_date: str = None,
    ):
        self.title = title
        self.project_id = project_id
        if description is not None:
            self.description = description
        if parent_task_id is not None:
            self.parent_task_id = parent_task_id
        if assignee_id is not None:
            self.assignee_id = assignee_id
        if done is not None:
            self.done = self._enum_matching(done, AddTaskRequestDone.list(), "done")
        if due_date is not None:
            self.due_date = due_date
