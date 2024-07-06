from __future__ import annotations
from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .action_post import ActionPost
from .scene_metadata import SceneMetadata
from .resource_identifier import ResourceIdentifier
from .scene_palette import ScenePalette


class ScenePostType(Enum):
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
        return list(map(lambda x: x.value, ScenePostType._member_map_.values()))


@JsonMap({"type_": "type"})
class ScenePost(BaseModel):
    """ScenePost

    :param type_: type_, defaults to None
    :type type_: ScenePostType, optional
    :param actions: List of actions to be executed synchronously on recall
    :type actions: List[ActionPost]
    :param metadata: metadata
    :type metadata: SceneMetadata
    :param group: group
    :type group: ResourceIdentifier
    :param palette: Group of colors that describe the palette of colors to be used when playing dynamics, defaults to None
    :type palette: ScenePalette, optional
    :param speed: Speed of dynamic palette for this scene, defaults to None
    :type speed: float, optional
    :param auto_dynamic: Indicates whether to automatically start the scene dynamically on active recall, defaults to None
    :type auto_dynamic: bool, optional
    """

    def __init__(
        self,
        actions: List[ActionPost],
        metadata: SceneMetadata,
        group: ResourceIdentifier,
        type_: ScenePostType = None,
        palette: ScenePalette = None,
        speed: float = None,
        auto_dynamic: bool = None,
    ):
        if type_ is not None:
            self.type_ = self._enum_matching(type_, ScenePostType.list(), "type_")
        self.actions = self._define_list(actions, ActionPost)
        self.metadata = self._define_object(metadata, SceneMetadata)
        self.group = self._define_object(group, ResourceIdentifier)
        if palette is not None:
            self.palette = self._define_object(palette, ScenePalette)
        if speed is not None:
            self.speed = speed
        if auto_dynamic is not None:
            self.auto_dynamic = auto_dynamic
