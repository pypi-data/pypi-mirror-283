from __future__ import annotations
from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .resource_identifier import ResourceIdentifier


class BridgeHomeGetType(Enum):
    """An enumeration representing different categories.

    :cvar BRIDGE_HOME: "bridge_home"
    :vartype BRIDGE_HOME: str
    """

    BRIDGE_HOME = "bridge_home"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, BridgeHomeGetType._member_map_.values()))


@JsonMap({"type_": "type", "id_": "id"})
class BridgeHomeGet(BaseModel):
    """BridgeHomeGet

    :param type_: type_, defaults to None
    :type type_: BridgeHomeGetType, optional
    :param id_: Unique identifier representing a specific resource instance, defaults to None
    :type id_: str, optional
    :param id_v1: Clip v1 resource identifier, defaults to None
    :type id_v1: str, optional
    :param children: Child devices/services to group by the derived group., defaults to None
    :type children: List[ResourceIdentifier], optional
    :param services: References all services aggregating control and state of children in the group.<br/>This includes all services grouped in the group hierarchy given by child relation.<br/>This includes all services of a device grouped in the group hierarchy given by child relation.<br/>Aggregation is per service type, ie every service type which can be grouped has a corresponding definition<br/>of grouped type Supported types: – grouped_light<br/>, defaults to None
    :type services: List[ResourceIdentifier], optional
    """

    def __init__(
        self,
        type_: BridgeHomeGetType = None,
        id_: str = None,
        id_v1: str = None,
        children: List[ResourceIdentifier] = None,
        services: List[ResourceIdentifier] = None,
    ):
        if type_ is not None:
            self.type_ = self._enum_matching(type_, BridgeHomeGetType.list(), "type_")
        if id_ is not None:
            self.id_ = self._pattern_matching(
                id_, "^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$", "id_"
            )
        if id_v1 is not None:
            self.id_v1 = self._pattern_matching(
                id_v1, "^(\/[a-z]{4,32}\/[0-9a-zA-Z-]{1,32})?$", "id_v1"
            )
        if children is not None:
            self.children = self._define_list(children, ResourceIdentifier)
        if services is not None:
            self.services = self._define_list(services, ResourceIdentifier)
