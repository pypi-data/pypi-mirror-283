from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.interaction_page import InteractionPage
from ..models.interaction_model import InteractionModel
from ..models.interaction_create_response import InteractionCreateResponse


class InteractionsService(BaseService):

    @cast_models
    def interaction_get_interaction(self, interaction_id: str) -> InteractionModel:
        """Retrieve a specific Interaction by providing the interactionId.

        :param interaction_id: interaction_id
        :type interaction_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Interaction
        :rtype: InteractionModel
        """

        Validator(str).validate(interaction_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/interactions/{{interactionId}}",
                self.get_default_headers(),
            )
            .add_path("interactionId", interaction_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return InteractionModel._unmap(response)

    @cast_models
    def interaction_delete_interaction(self, interaction_id: str):
        """Delete a specific Interaction by providing the interactionId.

        :param interaction_id: interaction_id
        :type interaction_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        """

        Validator(str).validate(interaction_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/interactions/{{interactionId}}",
                self.get_default_headers(),
            )
            .add_path("interactionId", interaction_id)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return response

    @cast_models
    def interaction_get_interactions(
        self, contact_id: str, schema_id: str, continuation: str = None
    ) -> InteractionPage:
        """Retrieve multiple Interactions of a specified type connected to a specific contactId. Both schemaId and contactId are required.
        The continuation parameter can be used to access the next page when there are more than 50 records available. This token can be found in the response.

        :param contact_id: contact_id
        :type contact_id: str
        :param schema_id: schema_id
        :type schema_id: str
        :param continuation: continuation, defaults to None
        :type continuation: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Interactions
        :rtype: InteractionPage
        """

        Validator(str).validate(contact_id)
        Validator(str).validate(schema_id)
        Validator(str).is_optional().validate(continuation)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/interactions", self.get_default_headers()
            )
            .add_query("contactId", contact_id)
            .add_query("schemaId", schema_id)
            .add_query("continuation", continuation)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return InteractionPage._unmap(response)

    @cast_models
    def interaction_create_interaction(
        self, request_body: any
    ) -> InteractionCreateResponse:
        """Create a new Interaction connected to a specific contactId.

        :param request_body: The request body.
        :type request_body: any
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: InteractionResponse
        :rtype: InteractionCreateResponse
        """

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/interactions", self.get_default_headers()
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return InteractionCreateResponse._unmap(response)
