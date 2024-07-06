from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.receipt import Receipt
from ..models.import_transactions_object import ImportTransactionsObject


class TransactionsService(BaseService):

    @cast_models
    def import_transactions_import_receipts(self, request_body: Receipt) -> dict:
        """The /receipts endpoint is used to store each customers purchase and returns in Engage.
        All fields in the data model can be used for segmentation and analysis in Engage.
        If you want to send out transactional emails, use the /orders endpoint instead.

        ### Identification

        To be able to store a receipt in Voyado, you need to connect it to a specific
        contact.

        In the example payload below the contact type is “Member” and the key type is “email”
        The key has to be a unique data field for the specific contact type,
        normally one of these fields:
        - contactId
        - email
        - mobilePhone
        - memberNumber
        - externalId
        - socialSecurityNumber (personal identity number - only Swedish or Finnish)

        :param request_body: The request body.
        :type request_body: Receipt
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return:
        :rtype: dict
        """

        Validator(Receipt).validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/api/v2/receipts", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return response

    @cast_models
    def import_transactions_import(
        self, request_body: ImportTransactionsObject
    ) -> dict:
        """Required on **receipt**:
        externalId (Unique receipt id), invoiceNumber, customerKey,
        customerKeyType, invoiceCreatedDate, InvoiceModifiedDate, StoreName, StoreNumber

        Required on **transaction**:
        externalId (Unique transaction id), articleNr, quantity, price and type (RETURN/DISCOUNT/PURCHASE)
        Note! It's recommended to include Sku, as it's a required
        attribute when enriching purchase data from article data.

        :param request_body: The request body.
        :type request_body: ImportTransactionsObject
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: dict
        """

        Validator(ImportTransactionsObject).validate(request_body)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/transactions", self.get_default_headers()
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return response
