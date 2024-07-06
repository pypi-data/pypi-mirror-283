from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .resource_identifier import ResourceIdentifier
from .room_archetype import RoomArchetype


@JsonMap({})
class RoomGetMetadata(BaseModel):
    """configuration object for a room

    :param name: Human readable name of a resource, defaults to None
    :type name: str, optional
    :param archetype: Possible archetypes of a room, defaults to None
    :type archetype: RoomArchetype, optional
    """

    def __init__(self, name: str = None, archetype: RoomArchetype = None):
        if name is not None:
            self.name = name
        if archetype is not None:
            self.archetype = self._enum_matching(
                archetype, RoomArchetype.list(), "archetype"
            )


@JsonMap({"type_": "type", "id_": "id"})
class RoomGet(BaseModel):
    """RoomGet

    :param type_: Type of the supported resources, defaults to None
    :type type_: str, optional
    :param id_: Unique identifier representing a specific resource instance, defaults to None
    :type id_: str, optional
    :param id_v1: Clip v1 resource identifier, defaults to None
    :type id_v1: str, optional
    :param children: Child devices/services to group by the derived group, defaults to None
    :type children: List[ResourceIdentifier], optional
    :param services: References all services aggregating control and state of children in the group.<br/>This includes all services grouped in the group hierarchy given by child relation.<br/>This includes all services of a device grouped in the group hierarchy given by child relation.<br/>Aggregation is per service type, ie every service type which can be grouped has a corresponding definition of<br/>grouped type.<br/>Supported types: – grouped_light<br/>, defaults to None
    :type services: List[ResourceIdentifier], optional
    :param metadata: configuration object for a room, defaults to None
    :type metadata: RoomGetMetadata, optional
    """

    def __init__(
        self,
        type_: str = None,
        id_: str = None,
        id_v1: str = None,
        children: List[ResourceIdentifier] = None,
        services: List[ResourceIdentifier] = None,
        metadata: RoomGetMetadata = None,
    ):
        if type_ is not None:
            self.type_ = type_
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
        if metadata is not None:
            self.metadata = self._define_object(metadata, RoomGetMetadata)
