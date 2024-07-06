from typing import List
from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.point_transaction_to_account_result_model import (
    PointTransactionToAccountResultModel,
)
from ..models.point_transaction_to_account import PointTransactionToAccount
from ..models.point_transaction_models_result import PointTransactionModelsResult
from ..models.point_transaction_model import PointTransactionModel
from ..models.point_definition_model import PointDefinitionModel
from ..models.point_account_point_transactions2_filter import (
    PointAccountPointTransactions2Filter,
)
from ..models.point_account_models_result import PointAccountModelsResult
from ..models.point_account_model import PointAccountModel


class PointAccountsService(BaseService):

    @cast_models
    def point_account_point_account_get(self, id_: int) -> PointAccountModel:
        """Get the point account by point account id

        :param id_: Account id
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: PointAccountModel
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/point-accounts/{{id}}",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return PointAccountModel._unmap(response)

    @cast_models
    def point_account_point_definition(self, id_: int) -> PointDefinitionModel:
        """## Gets a point account matched with the pointDefinitionId

        Gets the name, id and description for each pointDefinition

        :param id_: Definition Id
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: PointDefinitionModel
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/point-accounts/definitions/{{id}}",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return PointDefinitionModel._unmap(response)

    @cast_models
    def point_account_point_transactions(self, id_: int) -> PointTransactionModel:
        """point_account_point_transactions

        :param id_: Transaction id
        :type id_: int
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: PointTransactionModel
        """

        Validator(int).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/point-accounts/transactions/{{id}}",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return PointTransactionModel._unmap(response)

    @cast_models
    def point_account_point_definitions(
        self, offset: int = None, count: int = None
    ) -> List[PointDefinitionModel]:
        """## Gets point definitions

        :param offset: Defaults to 0, defaults to None
        :type offset: int, optional
        :param count: Defaults to 100, defaults to None
        :type count: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: List[PointDefinitionModel]
        """

        Validator(int).is_optional().validate(offset)
        Validator(int).is_optional().validate(count)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/point-accounts/definitions",
                self.get_default_headers(),
            )
            .add_query("offset", offset)
            .add_query("count", count)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return [PointDefinitionModel._unmap(item) for item in response]

    @cast_models
    def point_account_point_account_get2(
        self, contact_id: str, offset: int = None, count: int = None
    ) -> PointAccountModelsResult:
        """Gets a list of accounts by contact id

        :param contact_id: Contact id
        :type contact_id: str
        :param offset: Defaults to 0, defaults to None
        :type offset: int, optional
        :param count: Defaults to 100, defaults to None
        :type count: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: PointAccountModelsResult
        """

        Validator(str).validate(contact_id)
        Validator(int).is_optional().validate(offset)
        Validator(int).is_optional().validate(count)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/point-accounts", self.get_default_headers()
            )
            .add_query("contactId", contact_id)
            .add_query("offset", offset)
            .add_query("count", count)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return PointAccountModelsResult._unmap(response)

    @cast_models
    def point_account_point_transactions2(
        self,
        contact_id: str = None,
        definition_id: int = None,
        account_id: int = None,
        offset: int = None,
        count: int = None,
        filter: PointAccountPointTransactions2Filter = None,
    ) -> PointTransactionModelsResult:
        """There are two ways to fetch the list of transactions:
        - Using just the accountId returns the transactions for that particular points account. If this is used, the parameters contactId and definitionId are not required. If they are given, they will just be ignored.
        - The other way is to specify both contactId and definitionId. Both must be given.

        The optional parameters offset and count can be used in both cases to paginate the results.
        The optional parameter filter can also be used to fetch active points, pending points or both.
        All parameters are added to the query string.

        :param contact_id: Contact id - Required together with definitionId if not using account id, defaults to None
        :type contact_id: str, optional
        :param definition_id: Definition id - Required together with contactId if not using account id, defaults to None
        :type definition_id: int, optional
        :param account_id: Account id - Required if contactId and definitionId is not provided, defaults to None
        :type account_id: int, optional
        :param offset: Defaults to 0, defaults to None
        :type offset: int, optional
        :param count: Defaults to 100, defaults to None
        :type count: int, optional
        :param filter: All, Active or Pending. If not specified it will default to All., defaults to None
        :type filter: PointAccountPointTransactions2Filter, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: PointTransactionModelsResult
        """

        Validator(str).is_optional().validate(contact_id)
        Validator(int).is_optional().validate(definition_id)
        Validator(int).is_optional().validate(account_id)
        Validator(int).is_optional().validate(offset)
        Validator(int).is_optional().validate(count)
        Validator(PointAccountPointTransactions2Filter).is_optional().validate(filter)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/point-accounts/transactions",
                self.get_default_headers(),
            )
            .add_query("contactId", contact_id)
            .add_query("definitionId", definition_id)
            .add_query("accountId", account_id)
            .add_query("offset", offset)
            .add_query("count", count)
            .add_query("filter", filter)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return PointTransactionModelsResult._unmap(response)

    @cast_models
    def point_account_add_point_transactions(
        self, request_body: List[PointTransactionToAccount], idempotency_key: str = None
    ) -> PointTransactionToAccountResultModel:
        """## Point transactions being sent to a contacts specified point account, the endpoint will able to take max 1000 transaction rows.

        ### The following fields should be provided and have certain rules:
        - contactId: Must be a Guid
        - amount: The amount of points, negative amounts are accepted.
        - definitionId: specifies to which point account each transaction should be sent to
        - timeStamp: If not provided then the default value is taken from the requestors system timezone.
        - source: Must be provided or else that specified transaction will not be accepted.
        - description: Must be provided or else that transaction will not be accepted.
        - validFrom: If not provided then the default value is taken from the requestors system timezone.
        - validTo: Specifies how long the points are valid

        ### Important info:
        If some rows are not correct it will still result in an accepted response code and be skipped. Please
        check the response for NotAccepted items

        ### Idempotency-Key:
        The idempotency key is a unique identifier included in the header of an HTTP request to ensure the idempotence of certain operations. An idempotent operation is one that produces the same result regardless of how many times it is executed with the same input.
        #### Purpose
        The primary purpose of the idempotency key is to enable safe retries of requests. In situations where a client needs to resend a request due to network issues or other transient failures, the idempotency key helps prevent unintended side effects by ensuring that repeated requests with the same key result in the same outcome.

        :param request_body: The request body.
        :type request_body: List[PointTransactionToAccount]
        :param idempotency_key: Optional, lasts for 24 hours, defaults to None
        :type idempotency_key: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The request is accepted
        :rtype: PointTransactionToAccountResultModel
        """

        Validator(PointTransactionToAccount).is_array().validate(request_body)
        Validator(str).is_optional().validate(idempotency_key)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/point-accounts/transactions",
                self.get_default_headers(),
            )
            .add_header("Idempotency-Key", idempotency_key)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return PointTransactionToAccountResultModel._unmap(response)
