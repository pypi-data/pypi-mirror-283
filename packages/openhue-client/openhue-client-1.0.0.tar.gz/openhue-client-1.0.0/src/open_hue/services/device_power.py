from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.get_device_powers_ok_response import GetDevicePowersOkResponse
from ..models.get_device_power_ok_response import GetDevicePowerOkResponse


class DevicePowerService(BaseService):

    @cast_models
    def get_device_powers(self) -> GetDevicePowersOkResponse:
        """List all available device powers

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Device Power Success Response
        :rtype: GetDevicePowersOkResponse
        """

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/device_power",
                self.get_default_headers(),
            )
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetDevicePowersOkResponse._unmap(response)

    @cast_models
    def get_device_power(self, device_id: str) -> GetDevicePowerOkResponse:
        """Get power details of a single device from its given `{deviceId}`.

        :param device_id: ID of the device
        :type device_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Device Success Response
        :rtype: GetDevicePowerOkResponse
        """

        Validator(str).validate(device_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/device_power/{{deviceId}}",
                self.get_default_headers(),
            )
            .add_path("deviceId", device_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetDevicePowerOkResponse._unmap(response)
