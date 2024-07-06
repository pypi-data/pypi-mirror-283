from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class AddDealParticipantRequest(BaseModel):
    """AddDealParticipantRequest

    :param person_id: The ID of the person
    :type person_id: int
    """

    def __init__(self, person_id: int):
        self.person_id = person_id
