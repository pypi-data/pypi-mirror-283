from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .error import Error
from .room_get import RoomGet


@JsonMap({})
class GetRoomOkResponse(BaseModel):
    """GetRoomOkResponse

    :param errors: errors, defaults to None
    :type errors: List[Error], optional
    :param data: data, defaults to None
    :type data: List[RoomGet], optional
    """

    def __init__(self, errors: List[Error] = None, data: List[RoomGet] = None):
        if errors is not None:
            self.errors = self._define_list(errors, Error)
        if data is not None:
            self.data = self._define_list(data, RoomGet)
