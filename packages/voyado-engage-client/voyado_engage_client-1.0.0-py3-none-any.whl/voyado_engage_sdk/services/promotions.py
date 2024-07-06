from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.status_code_result import StatusCodeResult
from ..models.redeem_body_model import RedeemBodyModel
from ..models.promotion_validity_model import PromotionValidityModel
from ..models.multichannel_promotion_model import MultichannelPromotionModel
from ..models.multichannel_base_promotion_model import MultichannelBasePromotionModel


class PromotionsService(BaseService):

    @cast_models
    def multichannel_promotions_get_by_id(self, id_: str) -> MultichannelPromotionModel:
        """Gets the multichannel promotion with the identifier which is set by Voyado

        :param id_: Promotion identifier from Voyado
        :type id_: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: MultichannelPromotionModel
        """

        Validator(str).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/promotions/multichannels/{{id}}",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return MultichannelPromotionModel._unmap(response)

    @cast_models
    def multichannel_promotions_update(
        self, request_body: MultichannelPromotionModel, id_: str
    ) -> MultichannelPromotionModel:
        """Updates an existing multichannel promotion.
        Only multichannel promotion in status 'Draft' can be updated.

        :param request_body: The request body.
        :type request_body: MultichannelPromotionModel
        :param id_: Voyado multichannel promotion identifier
        :type id_: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: MultichannelPromotionModel
        """

        Validator(MultichannelPromotionModel).validate(request_body)
        Validator(str).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/promotions/multichannels/{{id}}",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return MultichannelPromotionModel._unmap(response)

    @cast_models
    def multichannel_promotions_delete_by_id(self, id_: str) -> StatusCodeResult:
        """Only unassigned multichannel promotions can be deleted

        :param id_: Voyado identifier to a multichannel promotion
        :type id_: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: StatusCodeResult
        """

        Validator(str).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/promotions/multichannels/{{id}}",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return StatusCodeResult._unmap(response)

    @cast_models
    def multichannel_promotions_get_validity_by_id(
        self, id_: str
    ) -> PromotionValidityModel:
        """Gets the multichannel promotion with the identifier which is an internal reference for Voyado

        :param id_: Identifier inside of Voyado
        :type id_: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: PromotionValidityModel
        """

        Validator(str).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/promotions/multichannels/{{id}}/validity",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return PromotionValidityModel._unmap(response)

    @cast_models
    def multichannel_promotions_update_validity(
        self, request_body: PromotionValidityModel, id_: str
    ) -> MultichannelPromotionModel:
        """Updates duration of an existing multichannel promotion.
        Only multichannel promotion in status 'Draft' can be updated.

        :param request_body: The request body.
        :type request_body: PromotionValidityModel
        :param id_: Voyado multichannel promotion identifier
        :type id_: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: MultichannelPromotionModel
        """

        Validator(PromotionValidityModel).validate(request_body)
        Validator(str).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/promotions/multichannels/{{id}}/validity",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return MultichannelPromotionModel._unmap(response)

    @cast_models
    def multichannel_promotions_get_by_external_id(
        self, external_id: str
    ) -> MultichannelPromotionModel:
        """Gets the multichannel promotion with the identifier which is an external reference for Voyado

        :param external_id: External identifier outside of Voyado
        :type external_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: MultichannelPromotionModel
        """

        Validator(str).validate(external_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/promotions/multichannels",
                self.get_default_headers(),
            )
            .add_query("externalId", external_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return MultichannelPromotionModel._unmap(response)

    @cast_models
    def multichannel_promotions_create(
        self, request_body: MultichannelBasePromotionModel
    ) -> MultichannelPromotionModel:
        """Only creates multichannel promotion in status 'Draft'.

        :param request_body: The request body.
        :type request_body: MultichannelBasePromotionModel
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: Created
        :rtype: MultichannelPromotionModel
        """

        Validator(MultichannelBasePromotionModel).validate(request_body)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/promotions/multichannels",
                self.get_default_headers(),
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return MultichannelPromotionModel._unmap(response)

    @cast_models
    def multichannel_promotions_delete_by_external_id(
        self, external_id: str
    ) -> StatusCodeResult:
        """Only unassigned multichannel promotions can be deleted

        :param external_id: External identifier to a multichannel promotion
        :type external_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: StatusCodeResult
        """

        Validator(str).validate(external_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/promotions/multichannels",
                self.get_default_headers(),
            )
            .add_query("externalId", external_id)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return StatusCodeResult._unmap(response)

    @cast_models
    def multichannel_promotions_get_by_validity_external_id(
        self, external_id: str
    ) -> PromotionValidityModel:
        """Gets the multichannel promotion validity with the identifier which is an external reference for Voyado

        :param external_id: External identifier outside of Voyado
        :type external_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: PromotionValidityModel
        """

        Validator(str).validate(external_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/promotions/multichannels/validity",
                self.get_default_headers(),
            )
            .add_query("externalId", external_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return PromotionValidityModel._unmap(response)

    @cast_models
    def offer_promotions_redeem_by_promotion_id(
        self, request_body: RedeemBodyModel, promotion_id: str
    ) -> dict:
        """Redeem a promotion (multichannel offer or mobile swipe) for a Contact using the internal promotion Id

        Redemption channel can be POS, ECOM or OTHER.

        :param request_body: The request body.
        :type request_body: RedeemBodyModel
        :param promotion_id: The id of the promotion
        :type promotion_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: dict
        """

        Validator(RedeemBodyModel).validate(request_body)
        Validator(str).validate(promotion_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/promotions/codes/{{promotionId}}/redeem",
                self.get_default_headers(),
            )
            .add_path("promotionId", promotion_id)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return response

    @cast_models
    def offer_promotions_reactivate_promotion_code(self, id_: str) -> str:
        """Reactivate a redeemed reward voucher

        :param id_: The id of the reward voucher
        :type id_: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: str
        """

        Validator(str).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/promotions/reward-vouchers/{{id}}/reactivate",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .serialize()
            .set_method("POST")
        )

        response = self.send_request(serialized_request)

        return response
