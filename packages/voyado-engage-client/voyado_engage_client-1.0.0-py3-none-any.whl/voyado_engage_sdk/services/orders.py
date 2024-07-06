from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.status_code_result import StatusCodeResult
from ..models.order import Order


class OrdersService(BaseService):

    @cast_models
    def orders_register_order(self, request_body: Order) -> StatusCodeResult:
        """The /orders endpoint is used to trigger automation flows in Engage and send out information about the order to your end customers.
        It could be used, for example, for an order confirmation, delivery confirmation or a return confirmation from an e-commerce
        system or store. The endpoint is called every time a change happens that you want to act on in Engage. All the data needed must
        be sent with every call, since this endpoint saves no data concerning orders. If you need to save data, use the /receipts endpoint instead.

        Note that there is no check against previous requests of the same order,
        thus two identical requests to this endpoint will trigger any matching automation twice.

        To accept an order:
        - The different orderStatus and paymentStatus values must be configured in Voyado.
        - totalGrossPrice, totalTax, item quantities etc. must be correct and add up.

        If the order is not accepted, a response with HTTP Status Code 400 or 422 and an error code will be returned.

        :param request_body: The request body.
        :type request_body: Order
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Accepted
        :rtype: StatusCodeResult
        """

        Validator(Order).validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/api/v2/orders", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return StatusCodeResult._unmap(response)
