from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"_128": "128", "_512": "512"})
class PictureIdPictures20(BaseModel):
    """PictureIdPictures20

    :param _128: The URL of the 128*128 picture, defaults to None
    :type _128: str, optional
    :param _512: The URL of the 512*512 picture, defaults to None
    :type _512: str, optional
    """

    def __init__(self, _128: str = None, _512: str = None):
        if _128 is not None:
            self._128 = _128
        if _512 is not None:
            self._512 = _512


@JsonMap({"id_": "id"})
class DataPictureId14(BaseModel):
    """DataPictureId14

    :param id_: The ID of the picture associated with the item, defaults to None
    :type id_: int, optional
    :param item_type: The type of item the picture is related to, defaults to None
    :type item_type: str, optional
    :param item_id: The ID of related item, defaults to None
    :type item_id: int, optional
    :param active_flag: Whether the associated picture is active or not, defaults to None
    :type active_flag: bool, optional
    :param add_time: The add time of the picture, defaults to None
    :type add_time: str, optional
    :param update_time: The update time of the picture, defaults to None
    :type update_time: str, optional
    :param added_by_user_id: The ID of the user who added the picture, defaults to None
    :type added_by_user_id: int, optional
    :param pictures: pictures, defaults to None
    :type pictures: PictureIdPictures20, optional
    """

    def __init__(
        self,
        id_: int = None,
        item_type: str = None,
        item_id: int = None,
        active_flag: bool = None,
        add_time: str = None,
        update_time: str = None,
        added_by_user_id: int = None,
        pictures: PictureIdPictures20 = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if item_type is not None:
            self.item_type = item_type
        if item_id is not None:
            self.item_id = item_id
        if active_flag is not None:
            self.active_flag = active_flag
        if add_time is not None:
            self.add_time = add_time
        if update_time is not None:
            self.update_time = update_time
        if added_by_user_id is not None:
            self.added_by_user_id = added_by_user_id
        if pictures is not None:
            self.pictures = self._define_object(pictures, PictureIdPictures20)


@JsonMap({"picture_id": "PICTURE_ID"})
class AddPersonPictureOkResponseData(BaseModel):
    """The picture that is associated with the item

    :param picture_id: picture_id, defaults to None
    :type picture_id: DataPictureId14, optional
    """

    def __init__(self, picture_id: DataPictureId14 = None):
        if picture_id is not None:
            self.picture_id = self._define_object(picture_id, DataPictureId14)


@JsonMap({})
class AddPersonPictureOkResponse(BaseModel):
    """AddPersonPictureOkResponse

    :param success: If the response is successful or not, defaults to None
    :type success: bool, optional
    :param data: The picture that is associated with the item, defaults to None
    :type data: AddPersonPictureOkResponseData, optional
    """

    def __init__(
        self, success: bool = None, data: AddPersonPictureOkResponseData = None
    ):
        if success is not None:
            self.success = success
        if data is not None:
            self.data = self._define_object(data, AddPersonPictureOkResponseData)
