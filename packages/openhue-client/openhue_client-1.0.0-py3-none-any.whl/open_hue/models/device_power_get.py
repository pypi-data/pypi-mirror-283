from __future__ import annotations
from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel
from .resource_identifier import ResourceIdentifier


class BatteryState(Enum):
    """An enumeration representing different categories.

    :cvar NORMAL: "normal"
    :vartype NORMAL: str
    :cvar LOW: "low"
    :vartype LOW: str
    :cvar CRITICAL: "critical"
    :vartype CRITICAL: str
    """

    NORMAL = "normal"
    LOW = "low"
    CRITICAL = "critical"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, BatteryState._member_map_.values()))


@JsonMap({})
class PowerState(BaseModel):
    """PowerState

    :param battery_state: Status of the power source of a device, only for battery powered devices.<br/><br/>- `normal` – battery level is sufficient<br/>- `low` – battery level low, some features (e.g. software update) might stop working, please change battery soon<br/>- `critical` – battery level critical, device can fail any moment<br/>, defaults to None
    :type battery_state: BatteryState, optional
    :param battery_level: The current battery state in percent, only for battery powered devices., defaults to None
    :type battery_level: int, optional
    """

    def __init__(self, battery_state: BatteryState = None, battery_level: int = None):
        if battery_state is not None:
            self.battery_state = self._enum_matching(
                battery_state, BatteryState.list(), "battery_state"
            )
        if battery_level is not None:
            self.battery_level = battery_level


@JsonMap({"type_": "type", "id_": "id"})
class DevicePowerGet(BaseModel):
    """DevicePowerGet

    :param type_: Type of the supported resources, defaults to None
    :type type_: str, optional
    :param id_: Unique identifier representing a specific resource instance, defaults to None
    :type id_: str, optional
    :param id_v1: Clip v1 resource identifier, defaults to None
    :type id_v1: str, optional
    :param owner: owner, defaults to None
    :type owner: ResourceIdentifier, optional
    :param power_state: power_state, defaults to None
    :type power_state: PowerState, optional
    """

    def __init__(
        self,
        type_: str = None,
        id_: str = None,
        id_v1: str = None,
        owner: ResourceIdentifier = None,
        power_state: PowerState = None,
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
        if power_state is not None:
            self.power_state = self._define_object(power_state, PowerState)
