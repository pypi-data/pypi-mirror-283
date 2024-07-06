from __future__ import annotations
from .utils.json_map import JsonMap
from .base import BaseModel
from .resource_identifier import ResourceIdentifier


@JsonMap({})
class SceneMetadata(BaseModel):
    """SceneMetadata

    :param name: Human readable name of a resource, defaults to None
    :type name: str, optional
    :param image: image, defaults to None
    :type image: ResourceIdentifier, optional
    :param appdata: Application specific data. Free format string., defaults to None
    :type appdata: str, optional
    """

    def __init__(
        self, name: str = None, image: ResourceIdentifier = None, appdata: str = None
    ):
        if name is not None:
            self.name = name
        if image is not None:
            self.image = self._define_object(image, ResourceIdentifier)
        if appdata is not None:
            self.appdata = appdata
