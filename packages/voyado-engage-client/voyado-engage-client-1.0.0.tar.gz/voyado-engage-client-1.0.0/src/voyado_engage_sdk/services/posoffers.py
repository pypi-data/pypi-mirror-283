from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.redeemed_loyalty_bar_claim_model import RedeemedLoyaltyBarClaimModel
from ..models.paged_result_of_available_loyalty_bar_claim_model import (
    PagedResultOfAvailableLoyaltyBarClaimModel,
)
from ..models.paged_result_of_all_loyalty_bar_claim_model import (
    PagedResultOfAllLoyaltyBarClaimModel,
)


class PosoffersService(BaseService):

    @cast_models
    def pos_offer_get_all_pos_offers_by_key(
        self, key_value: str
    ) -> PagedResultOfAllLoyaltyBarClaimModel:
        """Get all POS offers for a contact. Expired, redeemed and available.

        Finds the contact by using a key value other than Contact Id. This can
        only be used for contact types with exactly ONE key.
        The contact key attribute is configured for each Voyado instance.

        :param key_value: Key value, e.g. ssn, externalId, memberNumber, phone number etc.
        :type key_value: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: PagedResultOfAllLoyaltyBarClaimModel
        """

        Validator(str).validate(key_value)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/bykey/{{keyValue}}/posoffers/all",
                self.get_default_headers(),
            )
            .add_path("keyValue", key_value)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return PagedResultOfAllLoyaltyBarClaimModel._unmap(response)

    @cast_models
    def pos_offer_get_available_pos_offers_by_key(
        self, key_value: str
    ) -> PagedResultOfAvailableLoyaltyBarClaimModel:
        """Get all available POS offers for a contact.
        Expired and redeemed offers are excluded.

        Finds the contact by using a key value other than Contact Id. This can
        only be used for contact types with exactly ONE key.
        The contact key attribute is configured for each Voyado instance.

        :param key_value: Key value, e.g. ssn, externalId, memberNumber, phone number etc.
        :type key_value: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: PagedResultOfAvailableLoyaltyBarClaimModel
        """

        Validator(str).validate(key_value)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/bykey/{{keyValue}}/posoffers/available",
                self.get_default_headers(),
            )
            .add_path("keyValue", key_value)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return PagedResultOfAvailableLoyaltyBarClaimModel._unmap(response)

    @cast_models
    def pos_offer_get_all_pos_offers_by_contact_type_and_key(
        self, key_value: str, contact_type: str
    ) -> PagedResultOfAllLoyaltyBarClaimModel:
        """Get all POS offers for a contact. Expired, redeemed and available.

        Finds the contact by using a key value other than Contact Id. This can
        only be used for contact types with exactly ONE key.
        The contact key attribute is configured for each Voyado instance.

        :param key_value: Key value, e.g. ssn, externalId, memberNumber, phone number etc.
        :type key_value: str
        :param contact_type: Contact type, e.g. "member".
        :type contact_type: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: PagedResultOfAllLoyaltyBarClaimModel
        """

        Validator(str).validate(key_value)
        Validator(str).validate(contact_type)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactType}}/bykey/{{keyValue}}/posoffers/all",
                self.get_default_headers(),
            )
            .add_path("keyValue", key_value)
            .add_path("contactType", contact_type)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return PagedResultOfAllLoyaltyBarClaimModel._unmap(response)

    @cast_models
    def pos_offer_get_available_pos_offers_by_contact_type_and_key(
        self, key_value: str, contact_type: str
    ) -> PagedResultOfAvailableLoyaltyBarClaimModel:
        """Get all available POS offers for a contact.
        Expired and redeemed offers are excluded.

        Finds the contact by using a key value other than Contact Id. This can
        only be used for contact types with exactly ONE key.
        The contact key attribute is configured for each Voyado instance.

        :param key_value: Key value, e.g. ssn, externalId, memberNumber, phone number etc.
        :type key_value: str
        :param contact_type: Contact type, e.g. "member".
        :type contact_type: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: PagedResultOfAvailableLoyaltyBarClaimModel
        """

        Validator(str).validate(key_value)
        Validator(str).validate(contact_type)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactType}}/bykey/{{keyValue}}/posoffers/available",
                self.get_default_headers(),
            )
            .add_path("keyValue", key_value)
            .add_path("contactType", contact_type)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return PagedResultOfAvailableLoyaltyBarClaimModel._unmap(response)

    @cast_models
    def pos_offer_get_all_pos_offers_for_contact(
        self, contact_id: str, offset: int = None, count: int = None
    ) -> PagedResultOfAllLoyaltyBarClaimModel:
        """Get all POS offers for a contact. Expired, redeemed and available.
        The result can be paginated, using the offset and
        count query parameters.
        Note: *expiresOn* is obsolete and is always **null**

        :param contact_id: Contact identifier (GUID).
        :type contact_id: str
        :param offset: The first item to retrieve. (Default value 0), defaults to None
        :type offset: int, optional
        :param count: The max number of items to retrieve. (Default value 100), defaults to None
        :type count: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: PagedResultOfAllLoyaltyBarClaimModel
        """

        Validator(str).validate(contact_id)
        Validator(int).is_optional().validate(offset)
        Validator(int).is_optional().validate(count)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactId}}/posoffers/all",
                self.get_default_headers(),
            )
            .add_path("contactId", contact_id)
            .add_query("offset", offset)
            .add_query("count", count)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return PagedResultOfAllLoyaltyBarClaimModel._unmap(response)

    @cast_models
    def pos_offer_get_available_pos_offers_for_contact(
        self, contact_id: str, offset: int = None, count: int = None
    ) -> PagedResultOfAvailableLoyaltyBarClaimModel:
        """Get all available POS offers for a contact.
        Expired and redeemed offers are excluded.

        The result can be paginated, using the offset and
        count query parameters.

        :param contact_id: Contact identifier (GUID).
        :type contact_id: str
        :param offset: The first item to retrieve. (Default value 0), defaults to None
        :type offset: int, optional
        :param count: The max number of items to retrieve. (Default value 100), defaults to None
        :type count: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: PagedResultOfAvailableLoyaltyBarClaimModel
        """

        Validator(str).validate(contact_id)
        Validator(int).is_optional().validate(offset)
        Validator(int).is_optional().validate(count)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactId}}/posoffers/available",
                self.get_default_headers(),
            )
            .add_path("contactId", contact_id)
            .add_query("offset", offset)
            .add_query("count", count)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return PagedResultOfAvailableLoyaltyBarClaimModel._unmap(response)

    @cast_models
    def pos_offer_redeem(
        self, id_: str, contact_id: str
    ) -> RedeemedLoyaltyBarClaimModel:
        """Redeems a POS offer for a Contact using the internal Contact Id

        :param id_: The id returned from the get operation (GUID)
        :type id_: str
        :param contact_id: Contact identifier (GUID).
        :type contact_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: RedeemedLoyaltyBarClaimModel
        """

        Validator(str).validate(id_)
        Validator(str).validate(contact_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactId}}/posoffers/{{id}}/redeem",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .add_path("contactId", contact_id)
            .serialize()
            .set_method("POST")
        )

        response = self.send_request(serialized_request)

        return RedeemedLoyaltyBarClaimModel._unmap(response)

    @cast_models
    def pos_offer_redeem_by_key(
        self, id_: str, key_value: str
    ) -> RedeemedLoyaltyBarClaimModel:
        """Redeems a POS offer for a Contact using the key for the contact type

        Finds the contact by using a key value other than Contact Id. This can
        only be used for contact types with exactly ONE key.
        The contact key attribute is configured for each Voyado instance.

        :param id_: The id returned from the get operation (GUID)
        :type id_: str
        :param key_value: Key value, e.g. ssn, externalId, memberNumber, phone number etc.
        :type key_value: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: RedeemedLoyaltyBarClaimModel
        """

        Validator(str).validate(id_)
        Validator(str).validate(key_value)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/bykey/{{keyValue}}/posoffers/{{id}}/redeem",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .add_path("keyValue", key_value)
            .serialize()
            .set_method("POST")
        )

        response = self.send_request(serialized_request)

        return RedeemedLoyaltyBarClaimModel._unmap(response)

    @cast_models
    def pos_offer_redeem_by_contact_type_and_key(
        self, id_: str, key_value: str, contact_type: str
    ) -> RedeemedLoyaltyBarClaimModel:
        """Redeems a POS offer for a Contact using the key for the contact type

        Finds the contact by using a key value other than Contact Id. This can
        only be used for contact types with exactly ONE key.
        The contact key attribute is configured for each Voyado instance.

        :param id_: The id returned from the get operation (GUID)
        :type id_: str
        :param key_value: Key value, e.g. ssn, externalId, memberNumber, phone number etc.
        :type key_value: str
        :param contact_type: Contact type, e.g. "member" or "contact".
        :type contact_type: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: RedeemedLoyaltyBarClaimModel
        """

        Validator(str).validate(id_)
        Validator(str).validate(key_value)
        Validator(str).validate(contact_type)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactType}}/bykey/{{keyValue}}/posoffers/{{id}}/redeem",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .add_path("keyValue", key_value)
            .add_path("contactType", contact_type)
            .serialize()
            .set_method("POST")
        )

        response = self.send_request(serialized_request)

        return RedeemedLoyaltyBarClaimModel._unmap(response)
