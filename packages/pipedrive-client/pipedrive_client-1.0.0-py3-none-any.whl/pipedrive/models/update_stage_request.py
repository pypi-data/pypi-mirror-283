from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class UpdateStageRequest(BaseModel):
    """UpdateStageRequest

    :param name: The name of the stage, defaults to None
    :type name: str, optional
    :param pipeline_id: The ID of the pipeline to add stage to, defaults to None
    :type pipeline_id: int, optional
    :param deal_probability: The success probability percentage of the deal. Used/shown when deal weighted values are used., defaults to None
    :type deal_probability: int, optional
    :param rotten_flag: Whether deals in this stage can become rotten, defaults to None
    :type rotten_flag: bool, optional
    :param rotten_days: The number of days the deals not updated in this stage would become rotten. Applies only if the `rotten_flag` is set., defaults to None
    :type rotten_days: int, optional
    :param order_nr: An order number for this stage. Order numbers should be used to order the stages in the pipeline., defaults to None
    :type order_nr: int, optional
    """

    def __init__(
        self,
        name: str = None,
        pipeline_id: int = None,
        deal_probability: int = None,
        rotten_flag: bool = None,
        rotten_days: int = None,
        order_nr: int = None,
    ):
        if name is not None:
            self.name = name
        if pipeline_id is not None:
            self.pipeline_id = pipeline_id
        if deal_probability is not None:
            self.deal_probability = deal_probability
        if rotten_flag is not None:
            self.rotten_flag = rotten_flag
        if rotten_days is not None:
            self.rotten_days = rotten_days
        if order_nr is not None:
            self.order_nr = order_nr
