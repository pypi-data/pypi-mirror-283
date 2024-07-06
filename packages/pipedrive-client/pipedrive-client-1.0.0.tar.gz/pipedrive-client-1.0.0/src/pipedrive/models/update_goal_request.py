from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class UpdateGoalRequestInterval(Enum):
    """An enumeration representing different categories.

    :cvar WEEKLY: "weekly"
    :vartype WEEKLY: str
    :cvar MONTHLY: "monthly"
    :vartype MONTHLY: str
    :cvar QUARTERLY: "quarterly"
    :vartype QUARTERLY: str
    :cvar YEARLY: "yearly"
    :vartype YEARLY: str
    """

    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, UpdateGoalRequestInterval._member_map_.values())
        )


@JsonMap({"type_": "type"})
class UpdateGoalRequest(BaseModel):
    """UpdateGoalRequest

    :param title: The title of the goal, defaults to None
    :type title: str, optional
    :param assignee: Who this goal is assigned to. It requires the following JSON structure: `{ "id": "1", "type": "person" }`. `type` can be either `person`, `company` or `team`. ID of the assignee person, company or team., defaults to None
    :type assignee: dict, optional
    :param type_: The type of the goal. It requires the following JSON structure: `{ "name": "deals_started", "params": { "pipeline_id": [1, 2], "activity_type_id": [9] } }`. Type can be one of: `deals_won`, `deals_progressed`, `activities_completed`, `activities_added`, `deals_started` or `revenue_forecast`. `params` can include `pipeline_id`, `stage_id` or `activity_type_id`. `stage_id` is related to only `deals_progressed` type of goals and `activity_type_id` to `activities_completed` or `activities_added` types of goals. The `pipeline_id` and `activity_type_id` need to be given as an array of integers. To track the goal in all pipelines, set `pipeline_id` as `null` and similarly, to track the goal for all activities, set `activity_type_id` as `null`.”, defaults to None
    :type type_: dict, optional
    :param expected_outcome: The expected outcome of the goal. Expected outcome can be tracked either by `quantity` or by `sum`. It requires the following JSON structure: `{ "target": "50", "tracking_metric": "quantity" }` or `{ "target": "50", "tracking_metric": "sum", "currency_id": 1 }`. `currency_id` should only be added to `sum` type of goals., defaults to None
    :type expected_outcome: dict, optional
    :param duration: The date when the goal starts and ends. It requires the following JSON structure: `{ "start": "2019-01-01", "end": "2022-12-31" }`. Date in format of YYYY-MM-DD. "end" can be set to `null` for an infinite, open-ended goal., defaults to None
    :type duration: dict, optional
    :param interval: The interval of the goal, defaults to None
    :type interval: UpdateGoalRequestInterval, optional
    """

    def __init__(
        self,
        title: str = None,
        assignee: dict = None,
        type_: dict = None,
        expected_outcome: dict = None,
        duration: dict = None,
        interval: UpdateGoalRequestInterval = None,
    ):
        if title is not None:
            self.title = title
        if assignee is not None:
            self.assignee = assignee
        if type_ is not None:
            self.type_ = type_
        if expected_outcome is not None:
            self.expected_outcome = expected_outcome
        if duration is not None:
            self.duration = duration
        if interval is not None:
            self.interval = self._enum_matching(
                interval, UpdateGoalRequestInterval.list(), "interval"
            )
