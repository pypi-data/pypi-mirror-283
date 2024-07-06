from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_zone_ok_response import UpdateZoneOkResponse
from ..models.room_put import RoomPut
from ..models.get_zones_ok_response import GetZonesOkResponse
from ..models.get_zone_ok_response import GetZoneOkResponse
from ..models.delete_zone_ok_response import DeleteZoneOkResponse
from ..models.create_zone_ok_response import CreateZoneOkResponse


class ZoneService(BaseService):

    @cast_models
    def get_zones(self) -> GetZonesOkResponse:
        """List all available zones

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Zone Success Response
        :rtype: GetZonesOkResponse
        """

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/zone", self.get_default_headers()
            )
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetZonesOkResponse._unmap(response)

    @cast_models
    def create_zone(self, request_body: RoomPut = None) -> CreateZoneOkResponse:
        """Create a new zone

        :param request_body: The request body., defaults to None
        :type request_body: RoomPut, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: CreateZoneOkResponse
        """

        Validator(RoomPut).is_optional().validate(request_body)

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/zone", self.get_default_headers()
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return CreateZoneOkResponse._unmap(response)

    @cast_models
    def get_zone(self, zone_id: str) -> GetZoneOkResponse:
        """Get details of a single Zone from its given `{zoneId}`

        :param zone_id: ID of the Zone
        :type zone_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Zone Success Response
        :rtype: GetZoneOkResponse
        """

        Validator(str).validate(zone_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/zone/{{zoneId}}",
                self.get_default_headers(),
            )
            .add_path("zoneId", zone_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetZoneOkResponse._unmap(response)

    @cast_models
    def update_zone(
        self, zone_id: str, request_body: RoomPut = None
    ) -> UpdateZoneOkResponse:
        """Update a single Zone from its given `{zoneId}`

        :param request_body: The request body., defaults to None
        :type request_body: RoomPut, optional
        :param zone_id: ID of the Zone
        :type zone_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: UpdateZoneOkResponse
        """

        Validator(RoomPut).is_optional().validate(request_body)
        Validator(str).validate(zone_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/zone/{{zoneId}}",
                self.get_default_headers(),
            )
            .add_path("zoneId", zone_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateZoneOkResponse._unmap(response)

    @cast_models
    def delete_zone(self, zone_id: str) -> DeleteZoneOkResponse:
        """Delete a single Zone from its given `{zoneId}`

        :param zone_id: ID of the Zone
        :type zone_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: DeleteZoneOkResponse
        """

        Validator(str).validate(zone_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/zone/{{zoneId}}",
                self.get_default_headers(),
            )
            .add_path("zoneId", zone_id)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteZoneOkResponse._unmap(response)
