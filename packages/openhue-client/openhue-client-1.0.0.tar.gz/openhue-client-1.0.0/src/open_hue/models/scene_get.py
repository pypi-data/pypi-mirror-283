from __future__ import annotations
from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .resource_identifier import ResourceIdentifier
from .action_get import ActionGet
from .scene_metadata import SceneMetadata
from .scene_palette import ScenePalette


class SceneGetType(Enum):
    """An enumeration representing different categories.

    :cvar SCENE: "scene"
    :vartype SCENE: str
    """

    SCENE = "scene"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, SceneGetType._member_map_.values()))


class Active(Enum):
    """An enumeration representing different categories.

    :cvar INACTIVE: "inactive"
    :vartype INACTIVE: str
    :cvar STATIC: "static"
    :vartype STATIC: str
    :cvar DYNAMIC_PALETTE: "dynamic_palette"
    :vartype DYNAMIC_PALETTE: str
    """

    INACTIVE = "inactive"
    STATIC = "static"
    DYNAMIC_PALETTE = "dynamic_palette"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, Active._member_map_.values()))


@JsonMap({})
class SceneGetStatus(BaseModel):
    """SceneGetStatus

    :param active: active, defaults to None
    :type active: Active, optional
    """

    def __init__(self, active: Active = None):
        if active is not None:
            self.active = self._enum_matching(active, Active.list(), "active")


@JsonMap({"type_": "type", "id_": "id"})
class SceneGet(BaseModel):
    """SceneGet

    :param type_: type_, defaults to None
    :type type_: SceneGetType, optional
    :param id_: Unique identifier representing a specific resource instance, defaults to None
    :type id_: str, optional
    :param id_v1: Clip v1 resource identifier, defaults to None
    :type id_v1: str, optional
    :param owner: owner, defaults to None
    :type owner: ResourceIdentifier, optional
    :param actions: List of actions to be executed synchronously on recall, defaults to None
    :type actions: List[ActionGet], optional
    :param metadata: metadata, defaults to None
    :type metadata: SceneMetadata, optional
    :param group: group, defaults to None
    :type group: ResourceIdentifier, optional
    :param palette: Group of colors that describe the palette of colors to be used when playing dynamics, defaults to None
    :type palette: ScenePalette, optional
    :param speed: Speed of dynamic palette for this scene, defaults to None
    :type speed: float, optional
    :param auto_dynamic: Indicates whether to automatically start the scene dynamically on active recall, defaults to None
    :type auto_dynamic: bool, optional
    :param status: status, defaults to None
    :type status: SceneGetStatus, optional
    """

    def __init__(
        self,
        type_: SceneGetType = None,
        id_: str = None,
        id_v1: str = None,
        owner: ResourceIdentifier = None,
        actions: List[ActionGet] = None,
        metadata: SceneMetadata = None,
        group: ResourceIdentifier = None,
        palette: ScenePalette = None,
        speed: float = None,
        auto_dynamic: bool = None,
        status: SceneGetStatus = None,
    ):
        if type_ is not None:
            self.type_ = self._enum_matching(type_, SceneGetType.list(), "type_")
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
        if actions is not None:
            self.actions = self._define_list(actions, ActionGet)
        if metadata is not None:
            self.metadata = self._define_object(metadata, SceneMetadata)
        if group is not None:
            self.group = self._define_object(group, ResourceIdentifier)
        if palette is not None:
            self.palette = self._define_object(palette, ScenePalette)
        if speed is not None:
            self.speed = speed
        if auto_dynamic is not None:
            self.auto_dynamic = auto_dynamic
        if status is not None:
            self.status = self._define_object(status, SceneGetStatus)
