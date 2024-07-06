from enum import Enum


class SupportedDynamicStatus(Enum):
    """An enumeration representing different categories.

    :cvar DYNAMIC_PALETTE: "dynamic_palette"
    :vartype DYNAMIC_PALETTE: str
    :cvar NONE: "none"
    :vartype NONE: str
    """

    DYNAMIC_PALETTE = "dynamic_palette"
    NONE = "none"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, SupportedDynamicStatus._member_map_.values())
        )
