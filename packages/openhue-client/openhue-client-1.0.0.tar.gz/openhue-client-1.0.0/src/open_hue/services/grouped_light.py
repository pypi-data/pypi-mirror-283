from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_grouped_light_ok_response import UpdateGroupedLightOkResponse
from ..models.grouped_light_put import GroupedLightPut
from ..models.get_grouped_lights_ok_response import GetGroupedLightsOkResponse
from ..models.get_grouped_light_ok_response import GetGroupedLightOkResponse


class GroupedLightService(BaseService):

    @cast_models
    def get_grouped_lights(self) -> GetGroupedLightsOkResponse:
        """List all grouped lights

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Grouped Light Success Response
        :rtype: GetGroupedLightsOkResponse
        """

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/grouped_light",
                self.get_default_headers(),
            )
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetGroupedLightsOkResponse._unmap(response)

    @cast_models
    def get_grouped_light(self, grouped_light_id: str) -> GetGroupedLightOkResponse:
        """Get details of a single grouped light from its given `{groupedLightId}`.

        :param grouped_light_id: ID of the grouped light
        :type grouped_light_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Grouped Light Success Response
        :rtype: GetGroupedLightOkResponse
        """

        Validator(str).validate(grouped_light_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/grouped_light/{{groupedLightId}}",
                self.get_default_headers(),
            )
            .add_path("groupedLightId", grouped_light_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetGroupedLightOkResponse._unmap(response)

    @cast_models
    def update_grouped_light(
        self, grouped_light_id: str, request_body: GroupedLightPut = None
    ) -> UpdateGroupedLightOkResponse:
        """Update a single grouped light from its given `{groupedLightId}`.

        :param request_body: The request body., defaults to None
        :type request_body: GroupedLightPut, optional
        :param grouped_light_id: ID of the light
        :type grouped_light_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: UpdateGroupedLightOkResponse
        """

        Validator(GroupedLightPut).is_optional().validate(request_body)
        Validator(str).validate(grouped_light_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/grouped_light/{{groupedLightId}}",
                self.get_default_headers(),
            )
            .add_path("groupedLightId", grouped_light_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateGroupedLightOkResponse._unmap(response)
