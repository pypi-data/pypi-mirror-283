from enum import Enum


class SupportedTimedEffects(Enum):
    """An enumeration representing different categories.

    :cvar SUNRISE: "sunrise"
    :vartype SUNRISE: str
    :cvar NO_EFFECT: "no_effect"
    :vartype NO_EFFECT: str
    """

    SUNRISE = "sunrise"
    NO_EFFECT = "no_effect"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, SupportedTimedEffects._member_map_.values()))
