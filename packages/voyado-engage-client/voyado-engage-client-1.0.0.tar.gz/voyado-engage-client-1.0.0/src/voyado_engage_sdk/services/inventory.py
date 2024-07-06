from typing import List
from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.subscription_request import SubscriptionRequest
from ..models.stock_level_request import StockLevelRequest


class InventoryService(BaseService):

    @cast_models
    def inventory_update_stock_level(self, request_body: StockLevelRequest) -> dict:
        """Update stock level for a specific SKU.

        Request model:
        - Sku*: Unique SKU of the product. E.g: "123XYZ"
        - Quantity*: The latest stock quantity of the product. E.g: 10
        - Locale: Culture code. A corresponding product feed should be configured. E.g: "sv-se"
        - ExternalId: External identifier. E.g: "SE-123XYZ"

        \* required

        :param request_body: The request body.
        :type request_body: StockLevelRequest
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: dict
        """

        Validator(StockLevelRequest).validate(request_body)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/inventory/stock-levels",
                self.get_default_headers(),
            )
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return response

    @cast_models
    def inventory_update_stock_levels(
        self, request_body: List[StockLevelRequest]
    ) -> dict:
        """Batch update of stock levels for multiple SKU's.

        Request model:
        - Sku*: Unique SKU of the product. E.g: "123XYZ"
        - Quantity*: The latest stock quantity of the product. E.g: 10
        - Locale: Culture code. A corresponding product feed should be configured. E.g: "sv-se"
        - ExternalId: External identifier. E.g: "SE-123XYZ"

        \* required

        :param request_body: The request body.
        :type request_body: List[StockLevelRequest]
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: dict
        """

        Validator(StockLevelRequest).is_array().validate(request_body)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/inventory/stock-levels/batch",
                self.get_default_headers(),
            )
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return response

    @cast_models
    def back_in_stock_subscription_subscribe(
        self, request_body: SubscriptionRequest
    ) -> dict:
        """Create a back in stock subscription for a specific SKU.

        Request model:
        - ContactId*: Contact id of the subscriber. E.g: "FF9FD9AF-6778-4714-B0FE-F6E6612840C8"
        - Sku*: Unique SKU of the product. E.g: "123XYZ"
        - Locale*: Culture code. A corresponding product feed should be configured. E.g: "sv-se"
        - ExternalId: External identifier. E.g: "SE-123XYZ"

        \* required

        :param request_body: The request body.
        :type request_body: SubscriptionRequest
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: dict
        """

        Validator(SubscriptionRequest).validate(request_body)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/inventory/backinstock/subscriptions",
                self.get_default_headers(),
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return response

    @cast_models
    def back_in_stock_subscription_unsubscribe(self, subscription_id: str) -> dict:
        """Delete a specific back in stock subscription.

        :param subscription_id: subscription_id
        :type subscription_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: dict
        """

        Validator(str).validate(subscription_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/inventory/backinstock/subscriptions/{{subscriptionId}}",
                self.get_default_headers(),
            )
            .add_path("subscriptionId", subscription_id)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return response
