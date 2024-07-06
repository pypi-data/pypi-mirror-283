from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.redeemed_bonus_check_model import RedeemedBonusCheckModel
from ..models.paged_result_of_redeemed_bonus_check_model import (
    PagedResultOfRedeemedBonusCheckModel,
)
from ..models.paged_result_of_available_bonus_check_model import (
    PagedResultOfAvailableBonusCheckModel,
)
from ..models.paged_result_of_all_bonus_check_model import (
    PagedResultOfAllBonusCheckModel,
)


class BonuschecksService(BaseService):

    @cast_models
    def bonus_checks_get_bonus_checks_for_contact(
        self, contact_id: str, offset: int = None, count: int = None
    ) -> PagedResultOfAllBonusCheckModel:
        """Get all bonus checks for a contact. Expired, redeemed and available.
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
        :rtype: PagedResultOfAllBonusCheckModel
        """

        Validator(str).validate(contact_id)
        Validator(int).is_optional().validate(offset)
        Validator(int).is_optional().validate(count)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactId}}/bonuschecks",
                self.get_default_headers(),
            )
            .add_path("contactId", contact_id)
            .add_query("offset", offset)
            .add_query("count", count)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return PagedResultOfAllBonusCheckModel._unmap(response)

    @cast_models
    def bonus_checks_get_redeemed_bonus_checks_for_contact(
        self, contact_id: str, offset: int = None, count: int = None
    ) -> PagedResultOfRedeemedBonusCheckModel:
        """Get redeemed bonus checks for a contact.
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
        :rtype: PagedResultOfRedeemedBonusCheckModel
        """

        Validator(str).validate(contact_id)
        Validator(int).is_optional().validate(offset)
        Validator(int).is_optional().validate(count)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactId}}/bonuschecks/redeemed",
                self.get_default_headers(),
            )
            .add_path("contactId", contact_id)
            .add_query("offset", offset)
            .add_query("count", count)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return PagedResultOfRedeemedBonusCheckModel._unmap(response)

    @cast_models
    def bonus_checks_get_available_bonus_checks(
        self, contact_id: str, offset: int = None, count: int = None
    ) -> PagedResultOfAvailableBonusCheckModel:
        """Get available bonus checks for a contact.

        Expired and redeemed bonus checks are excluded

        The result can be paginated, using the *offset*
        and *count* query parameters.

        :param contact_id: Contact identifier (GUID).
        :type contact_id: str
        :param offset: Number of items to skip. (Default value 0), defaults to None
        :type offset: int, optional
        :param count: Max number of items to take. (Default value 100), defaults to None
        :type count: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: PagedResultOfAvailableBonusCheckModel
        """

        Validator(str).validate(contact_id)
        Validator(int).is_optional().validate(offset)
        Validator(int).is_optional().validate(count)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactId}}/bonuschecks/available",
                self.get_default_headers(),
            )
            .add_path("contactId", contact_id)
            .add_query("offset", offset)
            .add_query("count", count)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return PagedResultOfAvailableBonusCheckModel._unmap(response)

    @cast_models
    def bonus_checks_redeem_bonus_check(
        self, contact_id: str, bonus_check_id: str
    ) -> RedeemedBonusCheckModel:
        """Redeem a bonus check for a certain contact.

        :param contact_id: Contact identifier (GUID).
        :type contact_id: str
        :param bonus_check_id: Bonus check identifier.
        :type bonus_check_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: RedeemedBonusCheckModel
        """

        Validator(str).validate(contact_id)
        Validator(str).validate(bonus_check_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactId}}/bonuschecks/{{bonusCheckId}}/redeem",
                self.get_default_headers(),
            )
            .add_path("contactId", contact_id)
            .add_path("bonusCheckId", bonus_check_id)
            .serialize()
            .set_method("POST")
        )

        response = self.send_request(serialized_request)

        return RedeemedBonusCheckModel._unmap(response)
