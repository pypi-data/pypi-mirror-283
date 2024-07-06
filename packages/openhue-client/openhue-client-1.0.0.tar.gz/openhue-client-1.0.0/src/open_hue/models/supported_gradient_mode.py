from enum import Enum


class SupportedGradientMode(Enum):
    """An enumeration representing different categories.

    :cvar INTERPOLATED_PALETTE: "interpolated_palette"
    :vartype INTERPOLATED_PALETTE: str
    :cvar INTERPOLATED_PALETTE_MIRRORED: "interpolated_palette_mirrored"
    :vartype INTERPOLATED_PALETTE_MIRRORED: str
    :cvar RANDOM_PIXELATED: "random_pixelated"
    :vartype RANDOM_PIXELATED: str
    """

    INTERPOLATED_PALETTE = "interpolated_palette"
    INTERPOLATED_PALETTE_MIRRORED = "interpolated_palette_mirrored"
    RANDOM_PIXELATED = "random_pixelated"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, SupportedGradientMode._member_map_.values()))
