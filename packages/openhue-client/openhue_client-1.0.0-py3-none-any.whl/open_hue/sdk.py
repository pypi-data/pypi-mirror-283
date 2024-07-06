from .services.auth import AuthService
from .services.resource import ResourceService
from .services.device import DeviceService
from .services.device_power import DevicePowerService
from .services.light import LightService
from .services.light_level import LightLevelService
from .services.motion import MotionService
from .services.grouped_light import GroupedLightService
from .services.bridge import BridgeService
from .services.bridge_home import BridgeHomeService
from .services.scene import SceneService
from .services.room import RoomService
from .services.zone import ZoneService
from .services.temperature import TemperatureService
from .net.environment import Environment


class OpenHue:
    def __init__(
        self,
        api_key: str = None,
        api_key_header: str = "X-API-KEY",
        base_url: str = Environment.DEFAULT.value,
    ):
        """
        Initializes OpenHue the SDK class.
        """
        self.auth = AuthService(base_url=base_url)
        self.resource = ResourceService(base_url=base_url)
        self.device = DeviceService(base_url=base_url)
        self.device_power = DevicePowerService(base_url=base_url)
        self.light = LightService(base_url=base_url)
        self.light_level = LightLevelService(base_url=base_url)
        self.motion = MotionService(base_url=base_url)
        self.grouped_light = GroupedLightService(base_url=base_url)
        self.bridge = BridgeService(base_url=base_url)
        self.bridge_home = BridgeHomeService(base_url=base_url)
        self.scene = SceneService(base_url=base_url)
        self.room = RoomService(base_url=base_url)
        self.zone = ZoneService(base_url=base_url)
        self.temperature = TemperatureService(base_url=base_url)
        self.set_api_key(api_key, api_key_header)

    def set_base_url(self, base_url):
        """
        Sets the base URL for the entire SDK.
        """
        self.auth.set_base_url(base_url)
        self.resource.set_base_url(base_url)
        self.device.set_base_url(base_url)
        self.device_power.set_base_url(base_url)
        self.light.set_base_url(base_url)
        self.light_level.set_base_url(base_url)
        self.motion.set_base_url(base_url)
        self.grouped_light.set_base_url(base_url)
        self.bridge.set_base_url(base_url)
        self.bridge_home.set_base_url(base_url)
        self.scene.set_base_url(base_url)
        self.room.set_base_url(base_url)
        self.zone.set_base_url(base_url)
        self.temperature.set_base_url(base_url)

        return self

    def set_api_key(self, api_key: str, api_key_header="X-API-KEY"):
        """
        Sets the api key and the api key header for the entire SDK.
        """
        self.auth.set_api_key(api_key, api_key_header)
        self.resource.set_api_key(api_key, api_key_header)
        self.device.set_api_key(api_key, api_key_header)
        self.device_power.set_api_key(api_key, api_key_header)
        self.light.set_api_key(api_key, api_key_header)
        self.light_level.set_api_key(api_key, api_key_header)
        self.motion.set_api_key(api_key, api_key_header)
        self.grouped_light.set_api_key(api_key, api_key_header)
        self.bridge.set_api_key(api_key, api_key_header)
        self.bridge_home.set_api_key(api_key, api_key_header)
        self.scene.set_api_key(api_key, api_key_header)
        self.room.set_api_key(api_key, api_key_header)
        self.zone.set_api_key(api_key, api_key_header)
        self.temperature.set_api_key(api_key, api_key_header)

        return self


# c029837e0e474b76bc487506e8799df5e3335891efe4fb02bda7a1441840310c
