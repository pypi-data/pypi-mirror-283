from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models


class ContactoverviewService(BaseService):

    @cast_models
    def contact_overview_get_contact_overview_async(
        self,
        contact_type: str = None,
        contact_id: str = None,
        email: str = None,
        social_security_number: str = None,
        mobile_phone: str = None,
        custom_key: str = None,
        any: str = None,
    ) -> dict:
        """Get all information about a single contact by specifying either:
        - contactId
        - email and contactType
        - socialSecurityNumber and contactType
        - mobilePhone and contactType
        - customKey and contactType (the customKey must be configured by your supplier)
        - any and contactType - the any field can contain email, socialSecurityNumber, mobilePhone or the custom key (and are checked in that order)

        The dynamic fields of the response depend on your current Voyado configuration.

        :param contact_type: contact_type, defaults to None
        :type contact_type: str, optional
        :param contact_id: contact_id, defaults to None
        :type contact_id: str, optional
        :param email: email, defaults to None
        :type email: str, optional
        :param social_security_number: social_security_number, defaults to None
        :type social_security_number: str, optional
        :param mobile_phone: mobile_phone, defaults to None
        :type mobile_phone: str, optional
        :param custom_key: custom_key, defaults to None
        :type custom_key: str, optional
        :param any: any, defaults to None
        :type any: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: dict
        """

        Validator(str).is_optional().validate(contact_type)
        Validator(str).is_optional().validate(contact_id)
        Validator(str).is_optional().validate(email)
        Validator(str).is_optional().validate(social_security_number)
        Validator(str).is_optional().validate(mobile_phone)
        Validator(str).is_optional().validate(custom_key)
        Validator(str).is_optional().validate(any)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contactoverview", self.get_default_headers()
            )
            .add_query("contactType", contact_type)
            .add_query("contactId", contact_id)
            .add_query("email", email)
            .add_query("socialSecurityNumber", social_security_number)
            .add_query("mobilePhone", mobile_phone)
            .add_query("customKey", custom_key)
            .add_query("any", any)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return response
