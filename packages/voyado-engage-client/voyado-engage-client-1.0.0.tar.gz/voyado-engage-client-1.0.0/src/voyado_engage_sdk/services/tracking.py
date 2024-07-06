from typing import List
from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.product_view_api_model import ProductViewApiModel
from ..models.ok_result import OkResult
from ..models.cart_api_model import CartApiModel


class TrackingService(BaseService):

    @cast_models
    def cart_register_cart(self, request_body: CartApiModel) -> OkResult:
        """Register an update to a specific cart for a given contact. Should be the latest update of the cart.

        Request model:
        - CartReference: Unique identifier of the cart. Links the update to a specific cart. Ex: "006788ba-9f65-49c6-b3a0-2315d1854728"
        - Time: Time of the cart update. ISO8601 with Time Zone Designators. Ex: "2021-09-22T11:00:00+02:00"
        - ContactId: Contact id of the cart owner. GUID or short GUID. Ex: "ae16a9b4-f581-4568-8948-a96100b2afd4"
        - Language: Culture code of the cart. A corresponding product feed should be configured. Ex: "sv-SE"
        - Url: Url to the cart. Ex: "https://www.store.se/cart?id=006788ba-9f65-49c6-b3a0-2315d1854728"
        - Items: Collection of cart items. Ex: "[{"Sku":"90183744","Quantity":1},{"Sku":"90156607","Quantity":1}]"

        :param request_body: The request body.
        :type request_body: CartApiModel
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: OkResult
        """

        Validator(CartApiModel).validate(request_body)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/tracking/carts", self.get_default_headers()
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return OkResult._unmap(response)

    @cast_models
    def cart_register_carts(self, request_body: List[CartApiModel]) -> OkResult:
        """Register a batch of cart updates. Cart updates are processed according to update time. If multiple cart updates are registered with the same identifier only the latest update (according to update time) is considered.

        Request model:
        - CartReference: Unique identifier of the cart. Links the update to a specific cart. Ex: "006788ba-9f65-49c6-b3a0-2315d1854728"
        - Time: Time of the cart update. ISO8601 with Time Zone Designators. Ex: "2021-09-22T11:00:00+02:00"
        - ContactId: Contact id of the cart owner. GUID or short GUID. Ex: "ae16a9b4-f581-4568-8948-a96100b2afd4"
        - Language: Culture code of the cart. A corresponding product feed should be configured. Ex: "sv-SE"
        - Url: Url to the cart. Ex: "https://www.store.se/cart?id=006788ba-9f65-49c6-b3a0-2315d1854728"
        - Items: Collection of cart items. Ex: "[{"Sku":"90183744","Quantity":1},{"Sku":"90156607","Quantity":1}]"

        :param request_body: The request body.
        :type request_body: List[CartApiModel]
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: OkResult
        """

        Validator(CartApiModel).is_array().validate(request_body)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/tracking/carts/batch",
                self.get_default_headers(),
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return OkResult._unmap(response)

    @cast_models
    def product_view_v_register_product_view(
        self, request_body: ProductViewApiModel
    ) -> dict:
        """Register a view of a specific product for a given contact.

        Request model:
        - ItemId: Unique SKU/Article Id/Item Id of the viewed product. Will be matched against SKU on the imported articles in Voyado. Ex: "123XYZ"
        - Category: Category of the product on the website. Will be used for filtering. Ex: "novels &gt; cormac mccarthy &gt; the road"
        - Time: Time of the product view. ISO8601 with Time Zone Designators. Ex: "2021-09-22T11:00:00+02:00".
        - ContactId: Contact id of the viewer. GUID or short GUID. Ex: "FF9FD9AF-6778-4714-B0FE-F6E6612840C8"
        - SessionId: Unique identifier of the session. Ex: "3b7e493b-5dfe-4b98-b6cf-049f2ea4309d"
        - NewSession: Boolean value that indicates that new session.
        - Language: Culture code of the cart. A corresponding product feed should be configured. Ex: "sv-SE"
        - Url: Url of the productview. Ex: "https://www.voyado.com?sku=eu901-011-v10"
        - ExternalReferrer: The external site that the user came from (clicked a link) Ex: "https://www.google.com"

        :param request_body: The request body.
        :type request_body: ProductViewApiModel
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: dict
        """

        Validator(ProductViewApiModel).validate(request_body)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/tracking/productview",
                self.get_default_headers(),
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return response

    @cast_models
    def product_view_v_register_product_views(
        self, request_body: List[ProductViewApiModel]
    ) -> dict:
        """Register a collection of views to specific products for given contacts.

        Request model:
        - ItemId: Unique SKU/Article Id/Item Id of the viewed product. Will be matched against SKU on the imported articles in Voyado. Ex: "123XYZ"
        - Category: Category of the product on the website. Will be used for filtering. Ex: "novels &gt; cormac mccarthy &gt; the road"
        - Time: Time of the product view. ISO8601 with Time Zone Designators. Ex: "2021-09-22T11:00:00+02:00"
        - ContactId: Contact id of the viewer. GUID or short GUID. Ex: "FF9FD9AF-6778-4714-B0FE-F6E6612840C8"
        - SessionId: Unique identifier of the session. Ex: "3b7e493b-5dfe-4b98-b6cf-049f2ea4309d"
        - NewSession: Boolean value that indicates that new session.
        - Language: Culture code of the cart. A corresponding product feed should be configured. Ex: "sv-SE"
        - Url: Url of the productview. Ex: "https://www.voyado.com?sku=eu901-011-v10"
        - ExternalReferrer: The external site that the user came from (clicked a link) Ex: "https://www.google.com"

        :param request_body: The request body.
        :type request_body: List[ProductViewApiModel]
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: dict
        """

        Validator(ProductViewApiModel).is_array().validate(request_body)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/tracking/productviews",
                self.get_default_headers(),
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return response
