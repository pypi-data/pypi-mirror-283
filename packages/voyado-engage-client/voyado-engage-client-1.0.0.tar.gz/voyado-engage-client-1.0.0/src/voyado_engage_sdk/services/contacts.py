from typing import List
from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.redeem_body_model import RedeemBodyModel
from ..models.purchase_history_summary import PurchaseHistorySummary
from ..models.product_recommendations_model import ProductRecommendationsModel
from ..models.paged_result_of_transaction_item import PagedResultOfTransactionItem
from ..models.paged_result_of_bonus_point_transaction_model import (
    PagedResultOfBonusPointTransactionModel,
)
from ..models.paged_result_of_api_message import PagedResultOfApiMessage
from ..models.list_result_of_api_message import ListResultOfApiMessage
from ..models.i_api_contact import IApiContact
from ..models.change_type import ChangeType
from ..models.bool_request import BoolRequest
from ..models.api_promotion_model import ApiPromotionModel
from ..models.api_adjust_reward_points_response import ApiAdjustRewardPointsResponse
from ..models.api_adjust_reward_points import ApiAdjustRewardPoints


class ContactsService(BaseService):

    @cast_models
    def contacts_v_count(self) -> int:
        """Get number of approved contacts.

        This is a cached value that will be updated with a
        set frequency (normally once every 20 min).

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: int
        """

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/count", self.get_default_headers()
            )
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return response

    @cast_models
    def contacts_v_get_contact_by_id(self, contact_id: str) -> IApiContact:
        """Get a single contact, using the unique identifier.

        The dynamic fields of the response object depend on
        the current instance configuration.

        :param contact_id: Contact identifier (GUID).
        :type contact_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: IApiContact
        """

        Validator(str).validate(contact_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactId}}",
                self.get_default_headers(),
            )
            .add_path("contactId", contact_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return IApiContact._unmap(response)

    @cast_models
    def contacts_v_update_contact_post(
        self, request_body: any, contact_id: str
    ) -> IApiContact:
        """Update one or several fields of a single contact.
        Dont send an empty value unless you want it to be empty.

        :param request_body: The request body.
        :type request_body: any
        :param contact_id: Contact identifier (GUID).
        :type contact_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: IApiContact
        """

        Validator(str).validate(contact_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactId}}",
                self.get_default_headers(),
            )
            .add_path("contactId", contact_id)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return IApiContact._unmap(response)

    @cast_models
    def contacts_v_delete_with_header_param(
        self, contact_id: str, source: str = None
    ) -> dict:
        """contacts_v_delete_with_header_param

        :param contact_id: Contact identifier (GUID).
        :type contact_id: str
        :param source: Source system identifier (instance configuration), defaults to None
        :type source: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: dict
        """

        Validator(str).validate(contact_id)
        Validator(str).is_optional().validate(source)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactId}}",
                self.get_default_headers(),
            )
            .add_header("source", source)
            .add_path("contactId", contact_id)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return response

    @cast_models
    def contacts_v_count_by_contact_type(self, contact_type: str) -> int:
        """Get number of approved contacts of given type.

        This is a cached value that will be updated with a
        set frequency (normally once every 20 min).

        :param contact_type: Id for contact type, e.g. "member" or "contact"
        :type contact_type: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: int
        """

        Validator(str).validate(contact_type)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactType}}/count",
                self.get_default_headers(),
            )
            .add_path("contactType", contact_type)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return response

    @cast_models
    def contact_bulk_get_bulk_status(self, batch_id: str) -> dict:
        """contact_bulk_get_bulk_status

        :param batch_id: Id from bulk contact import
        :type batch_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Status object for batch
        :rtype: dict
        """

        Validator(str).validate(batch_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/bulk/status",
                self.get_default_headers(),
            )
            .add_query("batchId", batch_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return response

    @cast_models
    def contacts_v_get_contact_by_type_and_key_value_in_url_async(
        self, contact_type: str, key_value: str
    ) -> IApiContact:
        """! Please be aware that this endpoint is currently usable with either the key value being provided through !
        ! the path or a query param. Hence there being two of the same endpoints. !
        ! We recommend that you use the query param version (the first) as it is the more versatile one of the two !

        Get a single contact of a certain type, using a key
        value that corresponds to the current instance configuration. This can
        only be used for contact types with exactly ONE key.

        The dynamic fields of the response object depend on
        the current configuration.

        :param contact_type: Contact type, e.g. "member".
        :type contact_type: str
        :param key_value: Key value, e.g. ssn, phone number etc.
        :type key_value: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: IApiContact
        """

        Validator(str).validate(contact_type)
        Validator(str).validate(key_value)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactType}}/bykey/{{keyValue}}",
                self.get_default_headers(),
            )
            .add_path("contactType", contact_type)
            .add_path("keyValue", key_value)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return IApiContact._unmap(response)

    @cast_models
    def product_recommendation_get_product_recommendations(
        self, contact_id: str
    ) -> ProductRecommendationsModel:
        """product_recommendation_get_product_recommendations

        :param contact_id: Contact identifier (GUID).
        :type contact_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: ProductRecommendationsModel
        """

        Validator(str).validate(contact_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactId}}/productrecommendations",
                self.get_default_headers(),
            )
            .add_path("contactId", contact_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return ProductRecommendationsModel._unmap(response)

    @cast_models
    def contact_retail_kpi_get_purchase_history(
        self, contact_id: str
    ) -> PurchaseHistorySummary:
        """Following summary shows the purchase history for a single contact, over all time, 12 months and 24 months.

        :param contact_id: Contact identifier (GUID)
        :type contact_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: PurchaseHistorySummary
        """

        Validator(str).validate(contact_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactId}}/purchasehistorysummary",
                self.get_default_headers(),
            )
            .add_path("contactId", contact_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return PurchaseHistorySummary._unmap(response)

    @cast_models
    def back_in_stock_subscription_get_by_contact_id(self, contact_id: str):
        """Get back in stock subscriptions for a contact

        :param contact_id: contact_id
        :type contact_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        """

        Validator(str).validate(contact_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactId}}/backinstock/subscriptions",
                self.get_default_headers(),
            )
            .add_path("contactId", contact_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return response

    @cast_models
    def contacts_v_get_contact_by_external_id_async(
        self, contact_type: str, external_id: str
    ) -> IApiContact:
        """Get a single contact of a certain type, using the
        contact's external id.

        The dynamic fields of the response object depend on
        the current configuration.

        :param contact_type: Contact type, e.g. Member or Contact.
        :type contact_type: str
        :param external_id: External contact id.
        :type external_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: IApiContact
        """

        Validator(str).validate(contact_type)
        Validator(str).validate(external_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactType}}/byexternalid/{{externalId}}",
                self.get_default_headers(),
            )
            .add_path("contactType", contact_type)
            .add_path("externalId", external_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return IApiContact._unmap(response)

    @cast_models
    def contacts_v_get_contact_by_type_and_key_value_async(
        self, contact_type: str, key_value: str
    ) -> IApiContact:
        """Get a single contact of a certain type, using a key
        value that corresponds to the current instance configuration. This can
        only be used for contact types with exactly ONE key.

        The dynamic fields of the response object depend on
        the current configuration.

        :param contact_type: Contact type, e.g. "member".
        :type contact_type: str
        :param key_value: Key value, e.g. ssn, phone number etc.
        :type key_value: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: IApiContact
        """

        Validator(str).validate(contact_type)
        Validator(str).validate(key_value)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactType}}/bykey",
                self.get_default_headers(),
            )
            .add_path("contactType", contact_type)
            .add_query("keyValue", key_value)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return IApiContact._unmap(response)

    @cast_models
    def contact_message_get_latest_messages_by_contact_id(
        self, contact_id: str, count: int = None
    ) -> ListResultOfApiMessage:
        """Get the latest messages (max 500) a contact has received

        :param contact_id: Contact identifier (GUID).
        :type contact_id: str
        :param count: Max number of items to take. (Default value 100, Max value 500), defaults to None
        :type count: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: ListResultOfApiMessage
        """

        Validator(str).validate(contact_id)
        Validator(int).is_optional().validate(count)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactId}}/messages/latest",
                self.get_default_headers(),
            )
            .add_path("contactId", contact_id)
            .add_query("count", count)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return ListResultOfApiMessage._unmap(response)

    @cast_models
    def contact_message_get_messages_by_contact_id(
        self, contact_id: str, offset: int = None, count: int = None
    ) -> PagedResultOfApiMessage:
        """Optional offset and number of messages in response.

        :param contact_id: Contact identifier (GUID).
        :type contact_id: str
        :param offset: Default value 0, defaults to None
        :type offset: int, optional
        :param count: Max number of items to take. (Default value 100, max 500), defaults to None
        :type count: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: PagedResultOfApiMessage
        """

        Validator(str).validate(contact_id)
        Validator(int).is_optional().validate(offset)
        Validator(int).is_optional().validate(count)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactId}}/messages",
                self.get_default_headers(),
            )
            .add_path("contactId", contact_id)
            .add_query("offset", offset)
            .add_query("count", count)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return PagedResultOfApiMessage._unmap(response)

    @cast_models
    def transactions_get_transactions_by_contact_id(
        self, contact_id: str, offset: int = None, count: int = None
    ) -> PagedResultOfTransactionItem:
        """Get all purchase transactions for a single contact with
        optional offset and number of transactions in response.

        :param contact_id: Contact identifier (GUID)
        :type contact_id: str
        :param offset: Number of items to skip. (Default value 0), defaults to None
        :type offset: int, optional
        :param count: Max number of items to take. (Default value 100), defaults to None
        :type count: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: PagedResultOfTransactionItem
        """

        Validator(str).validate(contact_id)
        Validator(int).is_optional().validate(offset)
        Validator(int).is_optional().validate(count)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactId}}/transactions",
                self.get_default_headers(),
            )
            .add_path("contactId", contact_id)
            .add_query("offset", offset)
            .add_query("count", count)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return PagedResultOfTransactionItem._unmap(response)

    @cast_models
    def bonus_point_transactions_get_bonus_point_transactions_for_contact(
        self, contact_id: str, offset: int = None, count: int = None
    ) -> PagedResultOfBonusPointTransactionModel:
        """bonus_point_transactions_get_bonus_point_transactions_for_contact

        :param contact_id: The contact identifier (GUID).
        :type contact_id: str
        :param offset: The first item to retrieve. (Default value 0), defaults to None
        :type offset: int, optional
        :param count: The max number of items to retrieve. (Default value 100), defaults to None
        :type count: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: PagedResultOfBonusPointTransactionModel
        """

        Validator(str).validate(contact_id)
        Validator(int).is_optional().validate(offset)
        Validator(int).is_optional().validate(count)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactId}}/bonuspointtransactions",
                self.get_default_headers(),
            )
            .add_path("contactId", contact_id)
            .add_query("offset", offset)
            .add_query("count", count)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return PagedResultOfBonusPointTransactionModel._unmap(response)

    @cast_models
    def contacts_v_get_changed_contact_ids(
        self, change_type: ChangeType, from_date: str, to_date: str = None
    ) -> dict:
        """contacts_v_get_changed_contact_ids

        :param change_type: Created, Updated or Deleted
        :type change_type: ChangeType
        :param from_date: Start of timespan (ex 2023-05-04 11:20:00.000)
        :type from_date: str
        :param to_date: End of timespan (Default the current time and date), defaults to None
        :type to_date: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: dict
        """

        Validator(ChangeType).validate(change_type)
        Validator(str).validate(from_date)
        Validator(str).is_optional().validate(to_date)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/changes", self.get_default_headers()
            )
            .add_query("changeType", change_type)
            .add_query("fromDate", from_date)
            .add_query("toDate", to_date)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return response

    @cast_models
    def offer_promotions_get_promotions_for_contact(
        self, contact_id: str, redemption_channel_type: str = None
    ) -> List[ApiPromotionModel]:
        """Get available promotions for a contact. To filter on redemptionChannelType add it as a query string
        ?redemptionChannelType=POS
        It can be POS, ECOM or OTHER

        :param contact_id: Contact identifier
        :type contact_id: str
        :param redemption_channel_type: Filter on redemptionChannelType it can be POS, ECOM or OTHER, defaults to None
        :type redemption_channel_type: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: List[ApiPromotionModel]
        """

        Validator(str).validate(contact_id)
        Validator(str).is_optional().validate(redemption_channel_type)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactId}}/promotions",
                self.get_default_headers(),
            )
            .add_path("contactId", contact_id)
            .add_query("redemptionChannelType", redemption_channel_type)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return [ApiPromotionModel._unmap(item) for item in response]

    @cast_models
    def contact_overview_get_contact_id_async(
        self,
        contact_type: str = None,
        email: str = None,
        social_security_number: str = None,
        mobile_phone: str = None,
        custom_key: str = None,
        any: str = None,
    ) -> str:
        """Get the contactId for one (or several) contacts using either:
        - email
        - socialSecurityNumber
        - mobilePhone
        - customKey (the customKey must be configured by your supplier)
        - any - the any field can contain email, socialSecurityNumber, mobilePhone or the custom key (and are checked in that order)

        :param contact_type: contact_type, defaults to None
        :type contact_type: str, optional
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
        :rtype: str
        """

        Validator(str).is_optional().validate(contact_type)
        Validator(str).is_optional().validate(email)
        Validator(str).is_optional().validate(social_security_number)
        Validator(str).is_optional().validate(mobile_phone)
        Validator(str).is_optional().validate(custom_key)
        Validator(str).is_optional().validate(any)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/id", self.get_default_headers()
            )
            .add_query("contactType", contact_type)
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

    @cast_models
    def contacts_v_create_contact_header_param(
        self,
        request_body: any,
        source: str = None,
        store_external_id: str = None,
        create_as_unapproved: str = None,
    ) -> IApiContact:
        """Create a new, approved contact.

        If the contacts key identifier (example: Email) already exists : returns the GUID of the first entry found.

        :param request_body: The request body.
        :type request_body: any
        :param source: Source system identifier (instance configuration), defaults to None
        :type source: str, optional
        :param store_external_id: The unique id code of the current store (and therefore also the recruited-by store). Not mandatory but strongly recommended., defaults to None
        :type store_external_id: str, optional
        :param create_as_unapproved: Contact is not approved on creation. (Default value false), defaults to None
        :type create_as_unapproved: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Created
        :rtype: IApiContact
        """

        Validator(str).is_optional().validate(source)
        Validator(str).is_optional().validate(store_external_id)
        Validator(str).is_optional().validate(create_as_unapproved)

        serialized_request = (
            Serializer(f"{self.base_url}/api/v2/contacts", self.get_default_headers())
            .add_header("source", source)
            .add_header("storeExternalId", store_external_id)
            .add_header("createAsUnapproved", create_as_unapproved)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return IApiContact._unmap(response)

    @cast_models
    def contacts_v_promote_to_member(
        self, request_body: any, contact_id: str, source: str = None
    ) -> IApiContact:
        """Promote a contact to a member with one or several required fields.

        :param request_body: The request body.
        :type request_body: any
        :param contact_id: Contact identifier (GUID).
        :type contact_id: str
        :param source: Source system identifier (instance configuration), defaults to None
        :type source: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: IApiContact
        """

        Validator(str).validate(contact_id)
        Validator(str).is_optional().validate(source)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactId}}/promoteToMember",
                self.get_default_headers(),
            )
            .add_header("source", source)
            .add_path("contactId", contact_id)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return IApiContact._unmap(response)

    @cast_models
    def contact_bulk_create_contacts_in_bulk(
        self, request_body: any, contact_type: str = None
    ) -> str:
        """contact_bulk_create_contacts_in_bulk

        :param request_body: The request body.
        :type request_body: any
        :param contact_type: Optional, if not set the default ContactType will be used, defaults to None
        :type contact_type: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: BatchId
        :rtype: str
        """

        Validator(str).is_optional().validate(contact_type)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/bulk", self.get_default_headers()
            )
            .add_query("contactType", contact_type)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return response

    @cast_models
    def contact_bulk_update_contacts_in_bulk(
        self,
        request_body: any,
        contact_type: str = None,
        avoid_triggering_export: bool = None,
    ) -> str:
        """contact_bulk_update_contacts_in_bulk

        :param request_body: The request body.
        :type request_body: any
        :param contact_type: Optional, if not set the default ContactType will be used, defaults to None
        :type contact_type: str, optional
        :param avoid_triggering_export: Optional, default value is false, defaults to None
        :type avoid_triggering_export: bool, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: BatchId
        :rtype: str
        """

        Validator(str).is_optional().validate(contact_type)
        Validator(bool).is_optional().validate(avoid_triggering_export)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/bulk", self.get_default_headers()
            )
            .add_query("contactType", contact_type)
            .add_query("avoidTriggeringExport", avoid_triggering_export)
            .serialize()
            .set_method("PATCH")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return response

    @cast_models
    def contact_preferences_accepts_sms(
        self, request_body: BoolRequest, contact_id: str
    ) -> IApiContact:
        """Update the preference that indicates whether or not
        a contact accepts to be contacted via sms. This will also approve an unapproved contact.
        The primary way of updating a contact preference is through the update contacts endpoint.

        :param request_body: The request body.
        :type request_body: BoolRequest
        :param contact_id: Contact identifier (GUID).
        :type contact_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: IApiContact
        """

        Validator(BoolRequest).validate(request_body)
        Validator(str).validate(contact_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactId}}/preferences/acceptsSms",
                self.get_default_headers(),
            )
            .add_path("contactId", contact_id)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return IApiContact._unmap(response)

    @cast_models
    def bonus_point_transactions_adjust_reward_points(
        self, request_body: ApiAdjustRewardPoints, contact_id: str
    ) -> ApiAdjustRewardPointsResponse:
        """Adds reward points to a contact.

        :param request_body: The request body.
        :type request_body: ApiAdjustRewardPoints
        :param contact_id: Contact identifier (GUID).
        :type contact_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: ApiAdjustRewardPointsResponse
        """

        Validator(ApiAdjustRewardPoints).validate(request_body)
        Validator(str).validate(contact_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactId}}/rewardpointtransaction",
                self.get_default_headers(),
            )
            .add_path("contactId", contact_id)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return ApiAdjustRewardPointsResponse._unmap(response)

    @cast_models
    def contact_preferences_accepts_email(
        self, request_body: BoolRequest, contact_id: str
    ) -> IApiContact:
        """Update the preference that indicates whether or not
        a contact accepts to be contacted via email. This will also approve an unapproved contact.
        The primary way of updating a contact preference is through the update contacts endpoint.

        :param request_body: The request body.
        :type request_body: BoolRequest
        :param contact_id: Contact identifier (GUID).
        :type contact_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: IApiContact
        """

        Validator(BoolRequest).validate(request_body)
        Validator(str).validate(contact_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactId}}/preferences/acceptsEmail",
                self.get_default_headers(),
            )
            .add_path("contactId", contact_id)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return IApiContact._unmap(response)

    @cast_models
    def contact_preferences_accepts_postal(
        self, request_body: BoolRequest, contact_id: str
    ) -> IApiContact:
        """Update the preference that indicates whether or not
        a contact accepts to be contacted via regular mail. This will also approve an unapproved contact.
        The primary way of updating a contact preference is through the update contacts endpoint.

        :param request_body: The request body.
        :type request_body: BoolRequest
        :param contact_id: Contact identifier (GUID).
        :type contact_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: IApiContact
        """

        Validator(BoolRequest).validate(request_body)
        Validator(str).validate(contact_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactId}}/preferences/acceptsPostal",
                self.get_default_headers(),
            )
            .add_path("contactId", contact_id)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return IApiContact._unmap(response)

    @cast_models
    def assign_promotion_assign(self, contact_id: str, promotion_id: str) -> dict:
        """Assign a promotion (multichannel offer only) to a Contact using the internal Contact Id
        and the id of the promotion

        :param contact_id: Contact identifier
        :type contact_id: str
        :param promotion_id: The id of the promotion
        :type promotion_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: dict
        """

        Validator(str).validate(contact_id)
        Validator(str).validate(promotion_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactId}}/promotions/{{promotionId}}/assign",
                self.get_default_headers(),
            )
            .add_path("contactId", contact_id)
            .add_path("promotionId", promotion_id)
            .serialize()
            .set_method("POST")
        )

        response = self.send_request(serialized_request)

        return response

    @cast_models
    def offer_promotions_redeem(
        self, request_body: RedeemBodyModel, contact_id: str, promotion_id: str
    ) -> dict:
        """Redeem a promotion (multichannel offer or mobile swipe) for a Contact using the internal Contact Id

        Redemption channel can be POS, ECOM or OTHER.

        :param request_body: The request body.
        :type request_body: RedeemBodyModel
        :param contact_id: Contact identifier
        :type contact_id: str
        :param promotion_id: The id of the promotion
        :type promotion_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: dict
        """

        Validator(RedeemBodyModel).validate(request_body)
        Validator(str).validate(contact_id)
        Validator(str).validate(promotion_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactId}}/promotions/{{promotionId}}/redeem",
                self.get_default_headers(),
            )
            .add_path("contactId", contact_id)
            .add_path("promotionId", promotion_id)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return response

    @cast_models
    def contact_message_sms_unsubscribe_contact(
        self, contact_id: str, message_id: str = None
    ) -> dict:
        """Optional messageId input if user wants to unsubscribe on specific message instead of last sent Sms

        :param contact_id: Contact identifier (GUID).
        :type contact_id: str
        :param message_id: Message Id (string)., defaults to None
        :type message_id: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: dict
        """

        Validator(str).validate(contact_id)
        Validator(str).is_optional().validate(message_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactId}}/unsubscribeSms",
                self.get_default_headers(),
            )
            .add_path("contactId", contact_id)
            .add_query("messageId", message_id)
            .serialize()
            .set_method("POST")
        )

        response = self.send_request(serialized_request)

        return response

    @cast_models
    def contact_message_email_unsubscribe_contact(
        self, contact_id: str, message_id: str = None
    ):
        """Optional messageId input if user wants to unsubscribe on specific message instead of last sent email

        :param contact_id: Contact identifier (GUID).
        :type contact_id: str
        :param message_id: Message Id (string)., defaults to None
        :type message_id: str, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        """

        Validator(str).validate(contact_id)
        Validator(str).is_optional().validate(message_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactId}}/unsubscribeEmail",
                self.get_default_headers(),
            )
            .add_path("contactId", contact_id)
            .add_query("messageId", message_id)
            .serialize()
            .set_method("POST")
        )

        response = self.send_request(serialized_request)

        return response

    @cast_models
    def contacts_v_update_contact_type(self, contact_id: str, contact_type_id: str):
        """Updates the contactType for a contact if all expected contact data is available

        :param contact_id: Contact identifier (GUID).
        :type contact_id: str
        :param contact_type_id: The ContactType id (string).
        :type contact_type_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        """

        Validator(str).validate(contact_id)
        Validator(str).validate(contact_type_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactId}}/updateContactType",
                self.get_default_headers(),
            )
            .add_path("contactId", contact_id)
            .add_query("contactTypeId", contact_type_id)
            .serialize()
            .set_method("POST")
        )

        response = self.send_request(serialized_request)

        return response
