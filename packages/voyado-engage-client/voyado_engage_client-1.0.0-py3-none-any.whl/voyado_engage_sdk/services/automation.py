from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models


class AutomationService(BaseService):

    @cast_models
    def custom_triggers_trigger_by_contact_id(
        self, request_body: dict, trigger_id: str, contact_id: str
    ) -> dict:
        """custom_triggers_trigger_by_contact_id

        :param request_body: The request body.
        :type request_body: dict
        :param trigger_id: trigger_id
        :type trigger_id: str
        :param contact_id: contact_id
        :type contact_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: dict
        """

        Validator(dict).validate(request_body)
        Validator(str).validate(trigger_id)
        Validator(str).validate(contact_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/automation/customTriggers/{{triggerId}}/triggerByContactId/{{contactId}}",
                self.get_default_headers(),
            )
            .add_path("triggerId", trigger_id)
            .add_path("contactId", contact_id)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return response

    @cast_models
    def custom_triggers_trigger_by_social_security_number(
        self, request_body: dict, trigger_id: str, ssn: str
    ) -> dict:
        """custom_triggers_trigger_by_social_security_number

        :param request_body: The request body.
        :type request_body: dict
        :param trigger_id: trigger_id
        :type trigger_id: str
        :param ssn: ssn
        :type ssn: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: dict
        """

        Validator(dict).validate(request_body)
        Validator(str).validate(trigger_id)
        Validator(str).validate(ssn)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/automation/customTriggers/{{triggerId}}/triggerBySocialSecurityNumber/{{ssn}}",
                self.get_default_headers(),
            )
            .add_path("triggerId", trigger_id)
            .add_path("ssn", ssn)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return response

    @cast_models
    def custom_triggers_trigger_by_external_contact_id(
        self, request_body: dict, trigger_id: str, external_id: str
    ) -> dict:
        """custom_triggers_trigger_by_external_contact_id

        :param request_body: The request body.
        :type request_body: dict
        :param trigger_id: trigger_id
        :type trigger_id: str
        :param external_id: external_id
        :type external_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: dict
        """

        Validator(dict).validate(request_body)
        Validator(str).validate(trigger_id)
        Validator(str).validate(external_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/automation/customTriggers/{{triggerId}}/triggerByExternalContactId/{{externalId}}",
                self.get_default_headers(),
            )
            .add_path("triggerId", trigger_id)
            .add_path("externalId", external_id)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return response

    @cast_models
    def custom_triggers_trigger_by_contact_type_and_key(
        self, request_body: dict, trigger_id: str, contact_type: str, key_value: str
    ) -> dict:
        """custom_triggers_trigger_by_contact_type_and_key

        :param request_body: The request body.
        :type request_body: dict
        :param trigger_id: trigger_id
        :type trigger_id: str
        :param contact_type: contact_type
        :type contact_type: str
        :param key_value: key_value
        :type key_value: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: dict
        """

        Validator(dict).validate(request_body)
        Validator(str).validate(trigger_id)
        Validator(str).validate(contact_type)
        Validator(str).validate(key_value)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/automation/customTriggers/{{triggerId}}/triggerByContactTypeAndKey/{{contactType}}/{{keyValue}}",
                self.get_default_headers(),
            )
            .add_path("triggerId", trigger_id)
            .add_path("contactType", contact_type)
            .add_path("keyValue", key_value)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return response
