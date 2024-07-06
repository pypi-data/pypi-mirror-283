from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.send_sms_response import SendSmsResponse
from ..models.send_sms_request import SendSmsRequest


class SmsService(BaseService):

    @cast_models
    def sms_messages_send_sms_to_phone_numbers(
        self, request_body: SendSmsRequest
    ) -> SendSmsResponse:
        """Send an SMS to one or multiple phone numbers.

        Phone numbers must be prefixed with a + and country code
        (e.g. +4670xxxxxxx for a Swedish mobile phone number).

        :param request_body: The request body.
        :type request_body: SendSmsRequest
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: SendSmsResponse
        """

        Validator(SendSmsRequest).validate(request_body)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/sms/sendToPhoneNumbers",
                self.get_default_headers(),
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return SendSmsResponse._unmap(response)
