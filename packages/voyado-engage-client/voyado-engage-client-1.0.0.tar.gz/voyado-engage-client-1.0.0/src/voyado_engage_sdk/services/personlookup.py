from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.contact_search_result import ContactSearchResult


class PersonlookupService(BaseService):

    @cast_models
    def person_lookup_get_person_lookup(
        self,
        social_security_number: str = None,
        phone_number: str = None,
        country_code: str = None,
    ) -> ContactSearchResult:
        """person_lookup_get_person_lookup

        :param social_security_number: String that contains social security number, defaults to None
        :type social_security_number: str, optional
        :param phone_number: String that contains mobile phone number, defaults to None
        :type phone_number: str, optional
        :param country_code: Country where the contact is registered, defaults to None
        :type country_code: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: ContactSearchResult
        """

        Validator(str).is_optional().validate(social_security_number)
        Validator(str).is_optional().validate(phone_number)
        Validator(str).is_optional().validate(country_code)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/personlookup/getpersonlookup",
                self.get_default_headers(),
            )
            .add_query("socialSecurityNumber", social_security_number)
            .add_query("phoneNumber", phone_number)
            .add_query("countryCode", country_code)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return ContactSearchResult._unmap(response)
