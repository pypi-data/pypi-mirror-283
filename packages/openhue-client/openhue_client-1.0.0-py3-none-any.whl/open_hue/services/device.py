from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_device_ok_response import UpdateDeviceOkResponse
from ..models.get_devices_ok_response import GetDevicesOkResponse
from ..models.get_device_ok_response import GetDeviceOkResponse
from ..models.device_put import DevicePut
from ..models.delete_device_ok_response import DeleteDeviceOkResponse


class DeviceService(BaseService):

    @cast_models
    def get_devices(self) -> GetDevicesOkResponse:
        """List all available devices

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Device Success Response
        :rtype: GetDevicesOkResponse
        """

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/device", self.get_default_headers()
            )
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetDevicesOkResponse._unmap(response)

    @cast_models
    def get_device(self, device_id: str) -> GetDeviceOkResponse:
        """Get details of a single device from its given `{deviceId}`.

        :param device_id: ID of the device
        :type device_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Device Success Response
        :rtype: GetDeviceOkResponse
        """

        Validator(str).validate(device_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/device/{{deviceId}}",
                self.get_default_headers(),
            )
            .add_path("deviceId", device_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetDeviceOkResponse._unmap(response)

    @cast_models
    def update_device(
        self, device_id: str, request_body: DevicePut = None
    ) -> UpdateDeviceOkResponse:
        """Update a single device from its given `{deviceId}`.

        :param request_body: The request body., defaults to None
        :type request_body: DevicePut, optional
        :param device_id: ID of the device
        :type device_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: UpdateDeviceOkResponse
        """

        Validator(DevicePut).is_optional().validate(request_body)
        Validator(str).validate(device_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/device/{{deviceId}}",
                self.get_default_headers(),
            )
            .add_path("deviceId", device_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateDeviceOkResponse._unmap(response)

    @cast_models
    def delete_device(self, device_id: str) -> DeleteDeviceOkResponse:
        """Delete a single Device from its given `{deviceId}`. The `bridge` device cannot be deleted.

        :param device_id: ID of the Device
        :type device_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: DeleteDeviceOkResponse
        """

        Validator(str).validate(device_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/device/{{deviceId}}",
                self.get_default_headers(),
            )
            .add_path("deviceId", device_id)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteDeviceOkResponse._unmap(response)
