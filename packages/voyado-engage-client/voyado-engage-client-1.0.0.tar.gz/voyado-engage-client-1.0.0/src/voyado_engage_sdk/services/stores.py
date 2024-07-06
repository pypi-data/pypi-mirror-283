from typing import List
from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.api_store import ApiStore


class StoresService(BaseService):

    @cast_models
    def stores_v_get_stores(self, include_inactive: bool = None) -> List[ApiStore]:
        """stores_v_get_stores

        :param include_inactive: Value indicating if the inactive stores should be included or not. (Default value = false), defaults to None
        :type include_inactive: bool, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: List[ApiStore]
        """

        Validator(bool).is_optional().validate(include_inactive)

        serialized_request = (
            Serializer(f"{self.base_url}/api/v2/stores", self.get_default_headers())
            .add_query("includeInactive", include_inactive)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return [ApiStore._unmap(item) for item in response]

    @cast_models
    def stores_v_create_store(self, request_body: ApiStore) -> ApiStore:
        """stores_v_create_store

        :param request_body: The request body.
        :type request_body: ApiStore
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: ApiStore
        """

        Validator(ApiStore).validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/api/v2/stores", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return ApiStore._unmap(response)

    @cast_models
    def stores_v_get_store(
        self, external_id: str, include_inactive: bool = None
    ) -> ApiStore:
        """stores_v_get_store

        :param external_id: The external id of the store to get.
        :type external_id: str
        :param include_inactive: Value indicating if the store can be inactive or not. (Default value = false), defaults to None
        :type include_inactive: bool, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: ApiStore
        """

        Validator(str).validate(external_id)
        Validator(bool).is_optional().validate(include_inactive)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/stores/{{externalId}}",
                self.get_default_headers(),
            )
            .add_path("externalId", external_id)
            .add_query("includeInactive", include_inactive)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return ApiStore._unmap(response)

    @cast_models
    def stores_v_update_store(
        self, request_body: ApiStore, external_id: str
    ) -> ApiStore:
        """Updates a store. externalId is the store identifier.

        :param request_body: The request body.
        :type request_body: ApiStore
        :param external_id: The external id of the store to update.
        :type external_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: ApiStore
        """

        Validator(ApiStore).validate(request_body)
        Validator(str).validate(external_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/stores/{{externalId}}",
                self.get_default_headers(),
            )
            .add_path("externalId", external_id)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return ApiStore._unmap(response)
