from enum import Enum


class ProductArchetype(Enum):
    """An enumeration representing different categories.

    :cvar BRIDGE_V2: "bridge_v2"
    :vartype BRIDGE_V2: str
    :cvar UNKNOWN_ARCHETYPE: "unknown_archetype"
    :vartype UNKNOWN_ARCHETYPE: str
    :cvar CLASSIC_BULB: "classic_bulb"
    :vartype CLASSIC_BULB: str
    :cvar SULTAN_BULB: "sultan_bulb"
    :vartype SULTAN_BULB: str
    :cvar FLOOD_BULB: "flood_bulb"
    :vartype FLOOD_BULB: str
    :cvar SPOT_BULB: "spot_bulb"
    :vartype SPOT_BULB: str
    :cvar CANDLE_BULB: "candle_bulb"
    :vartype CANDLE_BULB: str
    :cvar LUSTER_BULB: "luster_bulb"
    :vartype LUSTER_BULB: str
    :cvar PENDANT_ROUND: "pendant_round"
    :vartype PENDANT_ROUND: str
    :cvar PENDANT_LONG: "pendant_long"
    :vartype PENDANT_LONG: str
    :cvar CEILING_ROUND: "ceiling_round"
    :vartype CEILING_ROUND: str
    :cvar CEILING_SQUARE: "ceiling_square"
    :vartype CEILING_SQUARE: str
    :cvar FLOOR_SHADE: "floor_shade"
    :vartype FLOOR_SHADE: str
    :cvar FLOOR_LANTERN: "floor_lantern"
    :vartype FLOOR_LANTERN: str
    :cvar TABLE_SHADE: "table_shade"
    :vartype TABLE_SHADE: str
    :cvar RECESSED_CEILING: "recessed_ceiling"
    :vartype RECESSED_CEILING: str
    :cvar RECESSED_FLOOR: "recessed_floor"
    :vartype RECESSED_FLOOR: str
    :cvar SINGLE_SPOT: "single_spot"
    :vartype SINGLE_SPOT: str
    :cvar DOUBLE_SPOT: "double_spot"
    :vartype DOUBLE_SPOT: str
    :cvar TABLE_WASH: "table_wash"
    :vartype TABLE_WASH: str
    :cvar WALL_LANTERN: "wall_lantern"
    :vartype WALL_LANTERN: str
    :cvar WALL_SHADE: "wall_shade"
    :vartype WALL_SHADE: str
    :cvar FLEXIBLE_LAMP: "flexible_lamp"
    :vartype FLEXIBLE_LAMP: str
    :cvar GROUND_SPOT: "ground_spot"
    :vartype GROUND_SPOT: str
    :cvar WALL_SPOT: "wall_spot"
    :vartype WALL_SPOT: str
    :cvar PLUG: "plug"
    :vartype PLUG: str
    :cvar HUE_GO: "hue_go"
    :vartype HUE_GO: str
    :cvar HUE_LIGHTSTRIP: "hue_lightstrip"
    :vartype HUE_LIGHTSTRIP: str
    :cvar HUE_IRIS: "hue_iris"
    :vartype HUE_IRIS: str
    :cvar HUE_BLOOM: "hue_bloom"
    :vartype HUE_BLOOM: str
    :cvar BOLLARD: "bollard"
    :vartype BOLLARD: str
    :cvar WALL_WASHER: "wall_washer"
    :vartype WALL_WASHER: str
    :cvar HUE_PLAY: "hue_play"
    :vartype HUE_PLAY: str
    :cvar VINTAGE_BULB: "vintage_bulb"
    :vartype VINTAGE_BULB: str
    :cvar VINTAGE_CANDLE_BULB: "vintage_candle_bulb"
    :vartype VINTAGE_CANDLE_BULB: str
    :cvar ELLIPSE_BULB: "ellipse_bulb"
    :vartype ELLIPSE_BULB: str
    :cvar TRIANGLE_BULB: "triangle_bulb"
    :vartype TRIANGLE_BULB: str
    :cvar SMALL_GLOBE_BULB: "small_globe_bulb"
    :vartype SMALL_GLOBE_BULB: str
    :cvar LARGE_GLOBE_BULB: "large_globe_bulb"
    :vartype LARGE_GLOBE_BULB: str
    :cvar EDISON_BULB: "edison_bulb"
    :vartype EDISON_BULB: str
    :cvar CHRISTMAS_TREE: "christmas_tree"
    :vartype CHRISTMAS_TREE: str
    :cvar STRING_LIGHT: "string_light"
    :vartype STRING_LIGHT: str
    :cvar HUE_CENTRIS: "hue_centris"
    :vartype HUE_CENTRIS: str
    :cvar HUE_LIGHTSTRIP_TV: "hue_lightstrip_tv"
    :vartype HUE_LIGHTSTRIP_TV: str
    :cvar HUE_LIGHTSTRIP_PC: "hue_lightstrip_pc"
    :vartype HUE_LIGHTSTRIP_PC: str
    :cvar HUE_TUBE: "hue_tube"
    :vartype HUE_TUBE: str
    :cvar HUE_SIGNE: "hue_signe"
    :vartype HUE_SIGNE: str
    :cvar PENDANT_SPOT: "pendant_spot"
    :vartype PENDANT_SPOT: str
    :cvar CEILING_HORIZONTAL: "ceiling_horizontal"
    :vartype CEILING_HORIZONTAL: str
    :cvar CEILING_TUBE: "ceiling_tube"
    :vartype CEILING_TUBE: str
    """

    BRIDGE_V2 = "bridge_v2"
    UNKNOWN_ARCHETYPE = "unknown_archetype"
    CLASSIC_BULB = "classic_bulb"
    SULTAN_BULB = "sultan_bulb"
    FLOOD_BULB = "flood_bulb"
    SPOT_BULB = "spot_bulb"
    CANDLE_BULB = "candle_bulb"
    LUSTER_BULB = "luster_bulb"
    PENDANT_ROUND = "pendant_round"
    PENDANT_LONG = "pendant_long"
    CEILING_ROUND = "ceiling_round"
    CEILING_SQUARE = "ceiling_square"
    FLOOR_SHADE = "floor_shade"
    FLOOR_LANTERN = "floor_lantern"
    TABLE_SHADE = "table_shade"
    RECESSED_CEILING = "recessed_ceiling"
    RECESSED_FLOOR = "recessed_floor"
    SINGLE_SPOT = "single_spot"
    DOUBLE_SPOT = "double_spot"
    TABLE_WASH = "table_wash"
    WALL_LANTERN = "wall_lantern"
    WALL_SHADE = "wall_shade"
    FLEXIBLE_LAMP = "flexible_lamp"
    GROUND_SPOT = "ground_spot"
    WALL_SPOT = "wall_spot"
    PLUG = "plug"
    HUE_GO = "hue_go"
    HUE_LIGHTSTRIP = "hue_lightstrip"
    HUE_IRIS = "hue_iris"
    HUE_BLOOM = "hue_bloom"
    BOLLARD = "bollard"
    WALL_WASHER = "wall_washer"
    HUE_PLAY = "hue_play"
    VINTAGE_BULB = "vintage_bulb"
    VINTAGE_CANDLE_BULB = "vintage_candle_bulb"
    ELLIPSE_BULB = "ellipse_bulb"
    TRIANGLE_BULB = "triangle_bulb"
    SMALL_GLOBE_BULB = "small_globe_bulb"
    LARGE_GLOBE_BULB = "large_globe_bulb"
    EDISON_BULB = "edison_bulb"
    CHRISTMAS_TREE = "christmas_tree"
    STRING_LIGHT = "string_light"
    HUE_CENTRIS = "hue_centris"
    HUE_LIGHTSTRIP_TV = "hue_lightstrip_tv"
    HUE_LIGHTSTRIP_PC = "hue_lightstrip_pc"
    HUE_TUBE = "hue_tube"
    HUE_SIGNE = "hue_signe"
    PENDANT_SPOT = "pendant_spot"
    CEILING_HORIZONTAL = "ceiling_horizontal"
    CEILING_TUBE = "ceiling_tube"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, ProductArchetype._member_map_.values()))
