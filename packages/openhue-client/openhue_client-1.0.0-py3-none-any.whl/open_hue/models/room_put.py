from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .resource_identifier import ResourceIdentifier
from .room_archetype import RoomArchetype


@JsonMap({})
class RoomPutMetadata(BaseModel):
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


@JsonMap({"type_": "type"})
class RoomPut(BaseModel):
    """RoomPut

    :param type_: Type of the supported resources (always `room` here), defaults to None
    :type type_: str, optional
    :param children: Child devices/services to group by the derived group, defaults to None
    :type children: List[ResourceIdentifier], optional
    :param metadata: configuration object for a room, defaults to None
    :type metadata: RoomPutMetadata, optional
    """

    def __init__(
        self,
        type_: str = None,
        children: List[ResourceIdentifier] = None,
        metadata: RoomPutMetadata = None,
    ):
        if type_ is not None:
            self.type_ = type_
        if children is not None:
            self.children = self._define_list(children, ResourceIdentifier)
        if metadata is not None:
            self.metadata = self._define_object(metadata, RoomPutMetadata)
