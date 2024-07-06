from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class AddStageRequest(BaseModel):
    """AddStageRequest

    :param name: The name of the stage
    :type name: str
    :param pipeline_id: The ID of the pipeline to add stage to
    :type pipeline_id: int
    :param deal_probability: The success probability percentage of the deal. Used/shown when deal weighted values are used., defaults to None
    :type deal_probability: int, optional
    :param rotten_flag: Whether deals in this stage can become rotten, defaults to None
    :type rotten_flag: bool, optional
    :param rotten_days: The number of days the deals not updated in this stage would become rotten. Applies only if the `rotten_flag` is set., defaults to None
    :type rotten_days: int, optional
    """

    def __init__(
        self,
        name: str,
        pipeline_id: int,
        deal_probability: int = None,
        rotten_flag: bool = None,
        rotten_days: int = None,
    ):
        self.name = name
        self.pipeline_id = pipeline_id
        if deal_probability is not None:
            self.deal_probability = deal_probability
        if rotten_flag is not None:
            self.rotten_flag = rotten_flag
        if rotten_days is not None:
            self.rotten_days = rotten_days
