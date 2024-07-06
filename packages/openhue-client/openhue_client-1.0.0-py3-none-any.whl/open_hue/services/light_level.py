from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_light_level_ok_response import UpdateLightLevelOkResponse
from ..models.light_level_put import LightLevelPut
from ..models.get_light_levels_ok_response import GetLightLevelsOkResponse
from ..models.get_light_level_ok_response import GetLightLevelOkResponse


class LightLevelService(BaseService):

    @cast_models
    def get_light_levels(self) -> GetLightLevelsOkResponse:
        """List all available light levels.

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Light Level Success Response
        :rtype: GetLightLevelsOkResponse
        """

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/light_level",
                self.get_default_headers(),
            )
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetLightLevelsOkResponse._unmap(response)

    @cast_models
    def get_light_level(self, light_id: str) -> GetLightLevelOkResponse:
        """Get details of a single light from its given `{lightId}`.

        :param light_id: ID of the light
        :type light_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Light Level Success Response
        :rtype: GetLightLevelOkResponse
        """

        Validator(str).validate(light_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/light_level/{{lightId}}",
                self.get_default_headers(),
            )
            .add_path("lightId", light_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetLightLevelOkResponse._unmap(response)

    @cast_models
    def update_light_level(
        self, light_id: str, request_body: LightLevelPut = None
    ) -> UpdateLightLevelOkResponse:
        """Update a single light from its given `{lightId}`.

        :param request_body: The request body., defaults to None
        :type request_body: LightLevelPut, optional
        :param light_id: ID of the light
        :type light_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: UpdateLightLevelOkResponse
        """

        Validator(LightLevelPut).is_optional().validate(request_body)
        Validator(str).validate(light_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/light_level/{{lightId}}",
                self.get_default_headers(),
            )
            .add_path("lightId", light_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateLightLevelOkResponse._unmap(response)
