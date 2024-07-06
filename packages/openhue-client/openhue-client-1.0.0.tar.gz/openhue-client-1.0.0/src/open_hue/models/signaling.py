from __future__ import annotations
from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .color import Color


class Signal(Enum):
    """An enumeration representing different categories.

    :cvar NO_SIGNAL: "no_signal"
    :vartype NO_SIGNAL: str
    :cvar ON_OFF: "on_off"
    :vartype ON_OFF: str
    :cvar ON_OFF_COLOR: "on_off_color"
    :vartype ON_OFF_COLOR: str
    :cvar ALTERNATING: "alternating"
    :vartype ALTERNATING: str
    """

    NO_SIGNAL = "no_signal"
    ON_OFF = "on_off"
    ON_OFF_COLOR = "on_off_color"
    ALTERNATING = "alternating"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, Signal._member_map_.values()))


@JsonMap({})
class Signaling(BaseModel):
    """Feature containing basic signaling properties.

    :param signal: - `no_signal`: No signal is active. Write “no_signal” to stop active signal.<br/>- `on_off`: Toggles between max brightness and Off in fixed color.<br/>- `on_off_color`: Toggles between off and max brightness with color provided.<br/>- `alternating`: Alternates between 2 provided colors.<br/>, defaults to None
    :type signal: Signal, optional
    :param duration: Duration has a max of 65534000 ms and a stepsize of 1 second.<br/>Values inbetween steps will be rounded.<br/>Duration is ignored for `no_signal`.<br/>, defaults to None
    :type duration: int, optional
    :param color: List of colors to apply to the signal (not supported by all signals), defaults to None
    :type color: List[Color], optional
    """

    def __init__(
        self, signal: Signal = None, duration: int = None, color: List[Color] = None
    ):
        if signal is not None:
            self.signal = self._enum_matching(signal, Signal.list(), "signal")
        if duration is not None:
            self.duration = duration
        if color is not None:
            self.color = self._define_list(color, Color)
