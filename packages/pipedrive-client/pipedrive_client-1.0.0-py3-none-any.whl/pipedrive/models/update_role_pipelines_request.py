from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class UpdateRolePipelinesRequest(BaseModel):
    """UpdateRolePipelinesRequest

    :param visible_pipeline_ids: The pipeline IDs to make the pipelines visible (add) and/or hidden (remove) for the specified role. It requires the following JSON structure: `{ "add": "[1]", "remove": "[3, 4]" }`.
    :type visible_pipeline_ids: dict
    """

    def __init__(self, visible_pipeline_ids: dict):
        self.visible_pipeline_ids = visible_pipeline_ids
