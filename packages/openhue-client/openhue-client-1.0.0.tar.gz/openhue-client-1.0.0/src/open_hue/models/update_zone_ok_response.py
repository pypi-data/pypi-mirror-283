from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .error import Error
from .resource_identifier import ResourceIdentifier


@JsonMap({})
class UpdateZoneOkResponse(BaseModel):
    """UpdateZoneOkResponse

    :param errors: errors, defaults to None
    :type errors: List[Error], optional
    :param data: data, defaults to None
    :type data: List[ResourceIdentifier], optional
    """

    def __init__(
        self, errors: List[Error] = None, data: List[ResourceIdentifier] = None
    ):
        if errors is not None:
            self.errors = self._define_list(errors, Error)
        if data is not None:
            self.data = self._define_list(data, ResourceIdentifier)
