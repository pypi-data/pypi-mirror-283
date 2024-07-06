from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"type_": "type"})
class LightLevelPut(BaseModel):
    """LightLevelPut

    :param type_: Type of the supported resources (always `light_level` here), defaults to None
    :type type_: str, optional
    :param enabled: true when sensor is activated, false when deactivated, defaults to None
    :type enabled: bool, optional
    """

    def __init__(self, type_: str = None, enabled: bool = None):
        if type_ is not None:
            self.type_ = type_
        if enabled is not None:
            self.enabled = enabled
