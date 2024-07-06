from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.member_status_model import MemberStatusModel


class MemberstatusService(BaseService):

    @cast_models
    def member_status_v_get(self, query: str) -> MemberStatusModel:
        """Gets the first found member that matches the query.

        Operation to get member overview. Is usually called from
        POS after a member gives some identification information
        this method returns the status together with contactId (GUID)
        and memberNumber (if available). The contactId may be used
        to get detailed contact information.

        Common identification fields that may be used in the query:
        socialSecurityNumber, email, mobilePhone, memberNumber and externalId

        The language of the returned answer is controlled by the language setting of the user connected to the API-key.

        :param query: {fieldId}:{value}, e.g. email:test@test.com
        :type query: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: MemberStatusModel
        """

        Validator(str).validate(query)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/memberstatus", self.get_default_headers()
            )
            .add_query("query", query)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return MemberStatusModel._unmap(response)
