from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_light_ok_response import UpdateLightOkResponse
from ..models.light_put import LightPut
from ..models.get_lights_ok_response import GetLightsOkResponse
from ..models.get_light_ok_response import GetLightOkResponse


class LightService(BaseService):

    @cast_models
    def get_lights(self) -> GetLightsOkResponse:
        """List all available lights.

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Light Success Response
        :rtype: GetLightsOkResponse
        """

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/light", self.get_default_headers()
            )
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetLightsOkResponse._unmap(response)

    @cast_models
    def get_light(self, light_id: str) -> GetLightOkResponse:
        """Get details of a single light from its given `{lightId}`.

        :param light_id: ID of the light
        :type light_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Light Success Response
        :rtype: GetLightOkResponse
        """

        Validator(str).validate(light_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/light/{{lightId}}",
                self.get_default_headers(),
            )
            .add_path("lightId", light_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetLightOkResponse._unmap(response)

    @cast_models
    def update_light(
        self, light_id: str, request_body: LightPut = None
    ) -> UpdateLightOkResponse:
        """Update a single light from its given `{lightId}`.

        :param request_body: The request body., defaults to None
        :type request_body: LightPut, optional
        :param light_id: ID of the light
        :type light_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: UpdateLightOkResponse
        """

        Validator(LightPut).is_optional().validate(request_body)
        Validator(str).validate(light_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/light/{{lightId}}",
                self.get_default_headers(),
            )
            .add_path("lightId", light_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateLightOkResponse._unmap(response)
