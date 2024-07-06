from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class Rtype(Enum):
    """An enumeration representing different categories.

    :cvar DEVICE: "device"
    :vartype DEVICE: str
    :cvar BRIDGE_HOME: "bridge_home"
    :vartype BRIDGE_HOME: str
    :cvar ROOM: "room"
    :vartype ROOM: str
    :cvar ZONE: "zone"
    :vartype ZONE: str
    :cvar LIGHT: "light"
    :vartype LIGHT: str
    :cvar BUTTON: "button"
    :vartype BUTTON: str
    :cvar RELATIVE_ROTARY: "relative_rotary"
    :vartype RELATIVE_ROTARY: str
    :cvar TEMPERATURE: "temperature"
    :vartype TEMPERATURE: str
    :cvar LIGHT_LEVEL: "light_level"
    :vartype LIGHT_LEVEL: str
    :cvar MOTION: "motion"
    :vartype MOTION: str
    :cvar CAMERA_MOTION: "camera_motion"
    :vartype CAMERA_MOTION: str
    :cvar ENTERTAINMENT: "entertainment"
    :vartype ENTERTAINMENT: str
    :cvar CONTACT: "contact"
    :vartype CONTACT: str
    :cvar TAMPER: "tamper"
    :vartype TAMPER: str
    :cvar GROUPED_LIGHT: "grouped_light"
    :vartype GROUPED_LIGHT: str
    :cvar DEVICE_POWER: "device_power"
    :vartype DEVICE_POWER: str
    :cvar ZIGBEE_BRIDGE_CONNECTIVITY: "zigbee_bridge_connectivity"
    :vartype ZIGBEE_BRIDGE_CONNECTIVITY: str
    :cvar ZIGBEE_CONNECTIVITY: "zigbee_connectivity"
    :vartype ZIGBEE_CONNECTIVITY: str
    :cvar ZGP_CONNECTIVITY: "zgp_connectivity"
    :vartype ZGP_CONNECTIVITY: str
    :cvar BRIDGE: "bridge"
    :vartype BRIDGE: str
    :cvar ZIGBEE_DEVICE_DISCOVERY: "zigbee_device_discovery"
    :vartype ZIGBEE_DEVICE_DISCOVERY: str
    :cvar HOMEKIT: "homekit"
    :vartype HOMEKIT: str
    :cvar MATTER: "matter"
    :vartype MATTER: str
    :cvar MATTER_FABRIC: "matter_fabric"
    :vartype MATTER_FABRIC: str
    :cvar SCENE: "scene"
    :vartype SCENE: str
    :cvar ENTERTAINMENT_CONFIGURATION: "entertainment_configuration"
    :vartype ENTERTAINMENT_CONFIGURATION: str
    :cvar PUBLIC_IMAGE: "public_image"
    :vartype PUBLIC_IMAGE: str
    :cvar AUTH_V1: "auth_v1"
    :vartype AUTH_V1: str
    :cvar BEHAVIOR_SCRIPT: "behavior_script"
    :vartype BEHAVIOR_SCRIPT: str
    :cvar BEHAVIOR_INSTANCE: "behavior_instance"
    :vartype BEHAVIOR_INSTANCE: str
    :cvar GEOFENCE: "geofence"
    :vartype GEOFENCE: str
    :cvar GEOFENCE_CLIENT: "geofence_client"
    :vartype GEOFENCE_CLIENT: str
    :cvar GEOLOCATION: "geolocation"
    :vartype GEOLOCATION: str
    :cvar SMART_SCENE: "smart_scene"
    :vartype SMART_SCENE: str
    """

    DEVICE = "device"
    BRIDGE_HOME = "bridge_home"
    ROOM = "room"
    ZONE = "zone"
    LIGHT = "light"
    BUTTON = "button"
    RELATIVE_ROTARY = "relative_rotary"
    TEMPERATURE = "temperature"
    LIGHT_LEVEL = "light_level"
    MOTION = "motion"
    CAMERA_MOTION = "camera_motion"
    ENTERTAINMENT = "entertainment"
    CONTACT = "contact"
    TAMPER = "tamper"
    GROUPED_LIGHT = "grouped_light"
    DEVICE_POWER = "device_power"
    ZIGBEE_BRIDGE_CONNECTIVITY = "zigbee_bridge_connectivity"
    ZIGBEE_CONNECTIVITY = "zigbee_connectivity"
    ZGP_CONNECTIVITY = "zgp_connectivity"
    BRIDGE = "bridge"
    ZIGBEE_DEVICE_DISCOVERY = "zigbee_device_discovery"
    HOMEKIT = "homekit"
    MATTER = "matter"
    MATTER_FABRIC = "matter_fabric"
    SCENE = "scene"
    ENTERTAINMENT_CONFIGURATION = "entertainment_configuration"
    PUBLIC_IMAGE = "public_image"
    AUTH_V1 = "auth_v1"
    BEHAVIOR_SCRIPT = "behavior_script"
    BEHAVIOR_INSTANCE = "behavior_instance"
    GEOFENCE = "geofence"
    GEOFENCE_CLIENT = "geofence_client"
    GEOLOCATION = "geolocation"
    SMART_SCENE = "smart_scene"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, Rtype._member_map_.values()))


@JsonMap({})
class ResourceIdentifier(BaseModel):
    """ResourceIdentifier

    :param rid: The unique id of the referenced resource, defaults to None
    :type rid: str, optional
    :param rtype: The type of the referenced resource, defaults to None
    :type rtype: Rtype, optional
    """

    def __init__(self, rid: str = None, rtype: Rtype = None):
        if rid is not None:
            self.rid = self._pattern_matching(
                rid, "^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$", "rid"
            )
        if rtype is not None:
            self.rtype = self._enum_matching(rtype, Rtype.list(), "rtype")
