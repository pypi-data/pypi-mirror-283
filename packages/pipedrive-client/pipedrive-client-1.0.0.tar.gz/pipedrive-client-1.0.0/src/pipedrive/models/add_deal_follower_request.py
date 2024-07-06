from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class AddDealFollowerRequest(BaseModel):
    """AddDealFollowerRequest

    :param user_id: The ID of the user
    :type user_id: int
    """

    def __init__(self, user_id: int):
        self.user_id = user_id
