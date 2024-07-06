from enum import Enum


class SupportedEffects(Enum):
    """An enumeration representing different categories.

    :cvar PRISM: "prism"
    :vartype PRISM: str
    :cvar OPAL: "opal"
    :vartype OPAL: str
    :cvar GLISTEN: "glisten"
    :vartype GLISTEN: str
    :cvar SPARKLE: "sparkle"
    :vartype SPARKLE: str
    :cvar FIRE: "fire"
    :vartype FIRE: str
    :cvar CANDLE: "candle"
    :vartype CANDLE: str
    :cvar NO_EFFECT: "no_effect"
    :vartype NO_EFFECT: str
    """

    PRISM = "prism"
    OPAL = "opal"
    GLISTEN = "glisten"
    SPARKLE = "sparkle"
    FIRE = "fire"
    CANDLE = "candle"
    NO_EFFECT = "no_effect"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, SupportedEffects._member_map_.values()))
