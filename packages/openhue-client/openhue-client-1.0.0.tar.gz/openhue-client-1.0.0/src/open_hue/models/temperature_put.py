from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class TemperaturePutType(Enum):
    """An enumeration representing different categories.

    :cvar TEMPERATURE: "temperature"
    :vartype TEMPERATURE: str
    """

    TEMPERATURE = "temperature"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, TemperaturePutType._member_map_.values()))


@JsonMap({"type_": "type"})
class TemperaturePut(BaseModel):
    """TemperaturePut

    :param type_: Type of the supported resources (always `temperature` here), defaults to None
    :type type_: TemperaturePutType, optional
    :param enabled: true when sensor is activated, false when deactivated, defaults to None
    :type enabled: bool, optional
    """

    def __init__(self, type_: TemperaturePutType = None, enabled: bool = None):
        if type_ is not None:
            self.type_ = self._enum_matching(type_, TemperaturePutType.list(), "type_")
        if enabled is not None:
            self.enabled = enabled
