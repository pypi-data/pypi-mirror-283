from typing import List
from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.enrichment_variable_group import EnrichmentVariableGroup


class BisnodeService(BaseService):

    @cast_models
    def bisnode_v_get_enrichments(
        self, contact_id: str
    ) -> List[EnrichmentVariableGroup]:
        """bisnode_v_get_enrichments

        :param contact_id: Contact identifier
        :type contact_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: List[EnrichmentVariableGroup]
        """

        Validator(str).validate(contact_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/bisnode/{{contactId}}/enrichments",
                self.get_default_headers(),
            )
            .add_path("contactId", contact_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return [EnrichmentVariableGroup._unmap(item) for item in response]
