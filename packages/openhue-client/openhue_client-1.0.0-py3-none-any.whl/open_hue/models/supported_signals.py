from enum import Enum


class SupportedSignals(Enum):
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
        return list(map(lambda x: x.value, SupportedSignals._member_map_.values()))
