from typing import List
from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.interaction_schema_without_json_model import (
    InteractionSchemaWithoutJsonModel,
)
from ..models.interaction_schema_response import InteractionSchemaResponse
from ..models.interaction_schema_model import InteractionSchemaModel


class InteractionschemasService(BaseService):

    @cast_models
    def interaction_schema_get_interaction_schemas(
        self,
    ) -> List[InteractionSchemaWithoutJsonModel]:
        """Retrieve all InteractionSchemas.

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: InteractionSchemas
        :rtype: List[InteractionSchemaWithoutJsonModel]
        """

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/interactionschemas", self.get_default_headers()
            )
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return [InteractionSchemaWithoutJsonModel._unmap(item) for item in response]

    @cast_models
    def interaction_schema_create_interaction_schema(
        self, request_body: any
    ) -> InteractionSchemaResponse:
        """Create a new InteractionSchema.

        :param request_body: The request body.
        :type request_body: any
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: InteractionSchemaResponse
        :rtype: InteractionSchemaResponse
        """

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/interactionschemas", self.get_default_headers()
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return InteractionSchemaResponse._unmap(response)

    @cast_models
    def interaction_schema_get_interaction_schema(
        self, interaction_schema_id: str
    ) -> InteractionSchemaModel:
        """Retrieve a specific InteractionSchema by providing the schemaId.

        :param interaction_schema_id: interaction_schema_id
        :type interaction_schema_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: InteractionSchema
        :rtype: InteractionSchemaModel
        """

        Validator(str).validate(interaction_schema_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/interactionschemas/{{interactionSchemaId}}",
                self.get_default_headers(),
            )
            .add_path("interactionSchemaId", interaction_schema_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return InteractionSchemaModel._unmap(response)

    @cast_models
    def interaction_schema_delete_interaction_schema(self, interaction_schema_id: str):
        """Delete InteractionSchema by providing the schemaId.

        :param interaction_schema_id: interaction_schema_id
        :type interaction_schema_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        """

        Validator(str).validate(interaction_schema_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/interactionschemas/{{interactionSchemaId}}",
                self.get_default_headers(),
            )
            .add_path("interactionSchemaId", interaction_schema_id)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return response
