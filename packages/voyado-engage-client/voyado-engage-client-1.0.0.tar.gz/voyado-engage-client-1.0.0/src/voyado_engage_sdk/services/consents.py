from typing import List
from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.api_consent_definition import ApiConsentDefinition


class ConsentsService(BaseService):

    @cast_models
    def consents_get_consents(self) -> List[ApiConsentDefinition]:
        """Get all consents definitions

        Example of metaData for a Consent:

        "metaData": {
          "conditionText": {
            "sv-SE": "Svensk villkorstext",
            "en-GB": "English text to show for condition"
          },
          "displayText": {
            "sv-SE": "Svensk text att visa",
            "en-GB": "English text to display"
          },
          "linkText": {
            "sv-SE": "Svensk text att visa på länk",
            "en-GB": "English text to show on link"
          }
        }

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: List[ApiConsentDefinition]
        """

        serialized_request = (
            Serializer(f"{self.base_url}/api/v2/consents", self.get_default_headers())
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return [ApiConsentDefinition._unmap(item) for item in response]
