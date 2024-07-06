from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_motion_sensor_ok_response import UpdateMotionSensorOkResponse
from ..models.motion_put import MotionPut
from ..models.get_motion_sensors_ok_response import GetMotionSensorsOkResponse
from ..models.get_motion_sensor_ok_response import GetMotionSensorOkResponse


class MotionService(BaseService):

    @cast_models
    def get_motion_sensors(self) -> GetMotionSensorsOkResponse:
        """List all available motion sensors.

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Motion Success Response
        :rtype: GetMotionSensorsOkResponse
        """

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/motion", self.get_default_headers()
            )
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetMotionSensorsOkResponse._unmap(response)

    @cast_models
    def get_motion_sensor(self, motion_id: str) -> GetMotionSensorOkResponse:
        """Get details of a single motion sensor from its given `{motionId}`.

        :param motion_id: ID of the motion sensor
        :type motion_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Motion Success Response
        :rtype: GetMotionSensorOkResponse
        """

        Validator(str).validate(motion_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/motion/{{motionId}}",
                self.get_default_headers(),
            )
            .add_path("motionId", motion_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetMotionSensorOkResponse._unmap(response)

    @cast_models
    def update_motion_sensor(
        self, motion_id: str, request_body: MotionPut = None
    ) -> UpdateMotionSensorOkResponse:
        """Update a single motion sensor from its given `{motionId}`.

        :param request_body: The request body., defaults to None
        :type request_body: MotionPut, optional
        :param motion_id: Id of the motion sensor
        :type motion_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: UpdateMotionSensorOkResponse
        """

        Validator(MotionPut).is_optional().validate(request_body)
        Validator(str).validate(motion_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/motion/{{motionId}}",
                self.get_default_headers(),
            )
            .add_path("motionId", motion_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateMotionSensorOkResponse._unmap(response)
