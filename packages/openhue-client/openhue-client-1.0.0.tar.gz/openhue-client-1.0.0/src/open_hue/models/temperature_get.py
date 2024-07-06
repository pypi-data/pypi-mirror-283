from __future__ import annotations
from .utils.json_map import JsonMap
from .base import BaseModel
from .resource_identifier import ResourceIdentifier


@JsonMap({})
class TemperatureReport(BaseModel):
    """TemperatureReport

    :param changed: last time the value of this property is changed., defaults to None
    :type changed: str, optional
    :param temperature: Temperature in 1.00 degrees Celsius, defaults to None
    :type temperature: float, optional
    """

    def __init__(self, changed: str = None, temperature: float = None):
        if changed is not None:
            self.changed = changed
        if temperature is not None:
            self.temperature = temperature


@JsonMap({})
class Temperature(BaseModel):
    """Temperature

    :param temperature: Deprecated. Moved to Temperature_report/temperature, defaults to None
    :type temperature: float, optional
    :param temperature_valid: Deprecated. Indication whether the value presented in temperature is valid, defaults to None
    :type temperature_valid: bool, optional
    :param temperature_report: temperature_report, defaults to None
    :type temperature_report: TemperatureReport, optional
    """

    def __init__(
        self,
        temperature: float = None,
        temperature_valid: bool = None,
        temperature_report: TemperatureReport = None,
    ):
        if temperature is not None:
            self.temperature = temperature
        if temperature_valid is not None:
            self.temperature_valid = temperature_valid
        if temperature_report is not None:
            self.temperature_report = self._define_object(
                temperature_report, TemperatureReport
            )


@JsonMap({"type_": "type", "id_": "id"})
class TemperatureGet(BaseModel):
    """TemperatureGet

    :param type_: Type of the supported resources, defaults to None
    :type type_: str, optional
    :param id_: Unique identifier representing a specific resource instance, defaults to None
    :type id_: str, optional
    :param id_v1: Clip v1 resource identifier, defaults to None
    :type id_v1: str, optional
    :param owner: owner, defaults to None
    :type owner: ResourceIdentifier, optional
    :param enabled: `true` when sensor is activated, `false` when deactivated<br/>, defaults to None
    :type enabled: bool, optional
    :param temperature: temperature, defaults to None
    :type temperature: Temperature, optional
    """

    def __init__(
        self,
        type_: str = None,
        id_: str = None,
        id_v1: str = None,
        owner: ResourceIdentifier = None,
        enabled: bool = None,
        temperature: Temperature = None,
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
        if temperature is not None:
            self.temperature = self._define_object(temperature, Temperature)
