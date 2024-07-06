from __future__ import annotations
from .utils.json_map import JsonMap
from .base import BaseModel
from .resource_identifier import ResourceIdentifier


@JsonMap({})
class LightLevelReport(BaseModel):
    """LightLevelReport

    :param changed: last time the value of this property is changed., defaults to None
    :type changed: str, optional
    :param light_level: Light level in 10000*log10(lux) +1 measured by sensor.<br/>Logarithmic scale used because the human eye adjusts to light levels and small changes at low<br/>lux levels are more noticeable than at high lux levels.<br/>This allows use of linear scale configuration sliders.<br/>, defaults to None
    :type light_level: int, optional
    """

    def __init__(self, changed: str = None, light_level: int = None):
        if changed is not None:
            self.changed = changed
        if light_level is not None:
            self.light_level = light_level


@JsonMap({})
class Light(BaseModel):
    """Light

    :param light_level: Deprecated. Moved to light_level_report/light_level, defaults to None
    :type light_level: int, optional
    :param light_level_valid: Deprecated. Indication whether the value presented in light_level is valid, defaults to None
    :type light_level_valid: bool, optional
    :param light_level_report: light_level_report, defaults to None
    :type light_level_report: LightLevelReport, optional
    """

    def __init__(
        self,
        light_level: int = None,
        light_level_valid: bool = None,
        light_level_report: LightLevelReport = None,
    ):
        if light_level is not None:
            self.light_level = light_level
        if light_level_valid is not None:
            self.light_level_valid = light_level_valid
        if light_level_report is not None:
            self.light_level_report = self._define_object(
                light_level_report, LightLevelReport
            )


@JsonMap({"type_": "type", "id_": "id"})
class LightLevelGet(BaseModel):
    """LightLevelGet

    :param type_: Type of the supported resources, defaults to None
    :type type_: str, optional
    :param id_: Unique identifier representing a specific resource instance, defaults to None
    :type id_: str, optional
    :param id_v1: Clip v1 resource identifier, defaults to None
    :type id_v1: str, optional
    :param owner: owner, defaults to None
    :type owner: ResourceIdentifier, optional
    :param enabled: true when sensor is activated, false when deactivated, defaults to None
    :type enabled: bool, optional
    :param light: light, defaults to None
    :type light: Light, optional
    """

    def __init__(
        self,
        type_: str = None,
        id_: str = None,
        id_v1: str = None,
        owner: ResourceIdentifier = None,
        enabled: bool = None,
        light: Light = None,
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
        if owner is not None:
            self.owner = self._define_object(owner, ResourceIdentifier)
        if enabled is not None:
            self.enabled = enabled
        if light is not None:
            self.light = self._define_object(light, Light)
