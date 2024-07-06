from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.update_scene_ok_response import UpdateSceneOkResponse
from ..models.scene_put import ScenePut
from ..models.scene_post import ScenePost
from ..models.get_scenes_ok_response import GetScenesOkResponse
from ..models.get_scene_ok_response import GetSceneOkResponse
from ..models.delete_scene_ok_response import DeleteSceneOkResponse
from ..models.create_scene_ok_response import CreateSceneOkResponse


class SceneService(BaseService):

    @cast_models
    def get_scenes(self) -> GetScenesOkResponse:
        """List all available scenes

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Scene Success Response
        :rtype: GetScenesOkResponse
        """

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/scene", self.get_default_headers()
            )
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetScenesOkResponse._unmap(response)

    @cast_models
    def create_scene(self, request_body: ScenePost = None) -> CreateSceneOkResponse:
        """Creates a new scene

        :param request_body: The request body., defaults to None
        :type request_body: ScenePost, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: CreateSceneOkResponse
        """

        Validator(ScenePost).is_optional().validate(request_body)

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/scene", self.get_default_headers()
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return CreateSceneOkResponse._unmap(response)

    @cast_models
    def get_scene(self, scene_id: str) -> GetSceneOkResponse:
        """Get details of a single scene from its given `{sceneId}`

        :param scene_id: ID of the scene.
        :type scene_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Scene Success Response
        :rtype: GetSceneOkResponse
        """

        Validator(str).validate(scene_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/scene/{{sceneId}}",
                self.get_default_headers(),
            )
            .add_path("sceneId", scene_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return GetSceneOkResponse._unmap(response)

    @cast_models
    def update_scene(
        self, scene_id: str, request_body: ScenePut = None
    ) -> UpdateSceneOkResponse:
        """Update a single scene from its given `{sceneId}`

        :param request_body: The request body., defaults to None
        :type request_body: ScenePut, optional
        :param scene_id: ID of the scene.
        :type scene_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: UpdateSceneOkResponse
        """

        Validator(ScenePut).is_optional().validate(request_body)
        Validator(str).validate(scene_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/scene/{{sceneId}}",
                self.get_default_headers(),
            )
            .add_path("sceneId", scene_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return UpdateSceneOkResponse._unmap(response)

    @cast_models
    def delete_scene(self, scene_id: str) -> DeleteSceneOkResponse:
        """Delete a single scene from its given `{sceneId}`

        :param scene_id: ID of the scene.
        :type scene_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Success
        :rtype: DeleteSceneOkResponse
        """

        Validator(str).validate(scene_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/clip/v2/resource/scene/{{sceneId}}",
                self.get_default_headers(),
            )
            .add_path("sceneId", scene_id)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return DeleteSceneOkResponse._unmap(response)
