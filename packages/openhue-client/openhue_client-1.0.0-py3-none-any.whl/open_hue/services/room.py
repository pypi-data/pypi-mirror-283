from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_room_ok_response import UpdateRoomOkResponse
from ..models.room_put import RoomPut
from ..models.get_rooms_ok_response import GetRoomsOkResponse
from ..models.get_room_ok_response import GetRoomOkResponse
from ..models.delete_room_ok_response import DeleteRoomOkResponse
from ..models.create_room_ok_response import CreateRoomOkResponse


class RoomService(BaseService):

    @cast_models
    def get_rooms(self) -> GetRoomsOkResponse:
        """List all available rooms

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Room Success Response
        :rtype: GetRoomsOkResponse
        """

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/room", self.get_default_headers()
            )
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetRoomsOkResponse._unmap(response)

    @cast_models
    def create_room(self, request_body: RoomPut = None) -> CreateRoomOkResponse:
        """Create a new room

        :param request_body: The request body., defaults to None
        :type request_body: RoomPut, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: CreateRoomOkResponse
        """

        Validator(RoomPut).is_optional().validate(request_body)

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/room", self.get_default_headers()
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return CreateRoomOkResponse._unmap(response)

    @cast_models
    def get_room(self, room_id: str) -> GetRoomOkResponse:
        """Get details of a single room from its given `{roomId}`

        :param room_id: ID of the room
        :type room_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Room Success Response
        :rtype: GetRoomOkResponse
        """

        Validator(str).validate(room_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/room/{{roomId}}",
                self.get_default_headers(),
            )
            .add_path("roomId", room_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetRoomOkResponse._unmap(response)

    @cast_models
    def update_room(
        self, room_id: str, request_body: RoomPut = None
    ) -> UpdateRoomOkResponse:
        """Update a single room from its given `{roomId}`

        :param request_body: The request body., defaults to None
        :type request_body: RoomPut, optional
        :param room_id: ID of the room
        :type room_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: UpdateRoomOkResponse
        """

        Validator(RoomPut).is_optional().validate(request_body)
        Validator(str).validate(room_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/room/{{roomId}}",
                self.get_default_headers(),
            )
            .add_path("roomId", room_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateRoomOkResponse._unmap(response)

    @cast_models
    def delete_room(self, room_id: str) -> DeleteRoomOkResponse:
        """Delete a single room from its given `{roomId}`

        :param room_id: ID of the room
        :type room_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: DeleteRoomOkResponse
        """

        Validator(str).validate(room_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/room/{{roomId}}",
                self.get_default_headers(),
            )
            .add_path("roomId", room_id)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteRoomOkResponse._unmap(response)
