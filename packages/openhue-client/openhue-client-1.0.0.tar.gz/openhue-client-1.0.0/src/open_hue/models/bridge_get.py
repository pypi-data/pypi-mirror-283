from __future__ import annotations
from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel
from .resource_identifier import ResourceIdentifier


class BridgeGetType(Enum):
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
        return list(map(lambda x: x.value, BridgeGetType._member_map_.values()))


@JsonMap({})
class TimeZone(BaseModel):
    """TimeZone

    :param time_zone: Time zone where the user's home is located (as Olson ID)., defaults to None
    :type time_zone: str, optional
    """

    def __init__(self, time_zone: str = None):
        if time_zone is not None:
            self.time_zone = time_zone


@JsonMap({"type_": "type", "id_": "id"})
class BridgeGet(BaseModel):
    """BridgeGet

    :param type_: type_, defaults to None
    :type type_: BridgeGetType, optional
    :param id_: Unique identifier representing a specific resource instance, defaults to None
    :type id_: str, optional
    :param id_v1: Clip v1 resource identifier, defaults to None
    :type id_v1: str, optional
    :param owner: owner, defaults to None
    :type owner: ResourceIdentifier, optional
    :param bridge_id: Unique identifier of the bridge as printed on the device. Lower case (shouldn't it be upper case?), defaults to None
    :type bridge_id: str, optional
    :param time_zone: time_zone, defaults to None
    :type time_zone: TimeZone, optional
    """

    def __init__(
        self,
        type_: BridgeGetType = None,
        id_: str = None,
        id_v1: str = None,
        owner: ResourceIdentifier = None,
        bridge_id: str = None,
        time_zone: TimeZone = None,
    ):
        if type_ is not None:
            self.type_ = self._enum_matching(type_, BridgeGetType.list(), "type_")
        if id_ is not None:
            self.id_ = self._pattern_matching(
                id_, "^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$", "id_"
            )
        if id_v1 is not None:
            self.id_v1 = self._pattern_matching(
                id_v1, "^(\/[a-z]{4,32}\/[0-9a-zA-Z-]{1,32})?$", "id_v1"
            )
        if owner is not None:
            self.owner = self._define_object(owner, ResourceIdentifier)
        if bridge_id is not None:
            self.bridge_id = bridge_id
        if time_zone is not None:
            self.time_zone = self._define_object(time_zone, TimeZone)
