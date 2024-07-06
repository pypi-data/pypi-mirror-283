from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class BridgePutType(Enum):
    """An enumeration representing different categories.

    :cvar BRIDGE: "bridge"
    :vartype BRIDGE: str
    """

    BRIDGE = "bridge"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, BridgePutType._member_map_.values()))


@JsonMap({"type_": "type"})
class BridgePut(BaseModel):
    """BridgePut

    :param type_: type_, defaults to None
    :type type_: BridgePutType, optional
    """

    def __init__(self, type_: BridgePutType = None):
        if type_ is not None:
            self.type_ = self._enum_matching(type_, BridgePutType.list(), "type_")
