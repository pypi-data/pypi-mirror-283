from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class AddFileRequest(BaseModel):
    """AddFileRequest

    :param file: A single file, supplied in the multipart/form-data encoding and contained within the given boundaries
    :type file: any
    :param deal_id: The ID of the deal to associate file(s) with, defaults to None
    :type deal_id: int, optional
    :param person_id: The ID of the person to associate file(s) with, defaults to None
    :type person_id: int, optional
    :param org_id: The ID of the organization to associate file(s) with, defaults to None
    :type org_id: int, optional
    :param product_id: The ID of the product to associate file(s) with, defaults to None
    :type product_id: int, optional
    :param activity_id: The ID of the activity to associate file(s) with, defaults to None
    :type activity_id: int, optional
    :param lead_id: The ID of the lead to associate file(s) with, defaults to None
    :type lead_id: str, optional
    """

    def __init__(
        self,
        file: any,
        deal_id: int = None,
        person_id: int = None,
        org_id: int = None,
        product_id: int = None,
        activity_id: int = None,
        lead_id: str = None,
    ):
        self.file = file
        if deal_id is not None:
            self.deal_id = deal_id
        if person_id is not None:
            self.person_id = person_id
        if org_id is not None:
            self.org_id = org_id
        if product_id is not None:
            self.product_id = product_id
        if activity_id is not None:
            self.activity_id = activity_id
        if lead_id is not None:
            self.lead_id = lead_id
