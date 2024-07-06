from typing import List
from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.paged_result_of_api_achievement_definition import (
    PagedResultOfApiAchievementDefinition,
)
from ..models.api_achievement_value import ApiAchievementValue


class AchievementsService(BaseService):

    @cast_models
    def achievements_get_achievements_for_contact(
        self, contact_id: str
    ) -> List[ApiAchievementValue]:
        """achievements_get_achievements_for_contact

        :param contact_id: contact_id
        :type contact_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: List[ApiAchievementValue]
        """

        Validator(str).validate(contact_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactId}}/achievements",
                self.get_default_headers(),
            )
            .add_path("contactId", contact_id)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return [ApiAchievementValue._unmap(item) for item in response]

    @cast_models
    def achievements_get_all_achievements(
        self, offset: int = None, count: int = None
    ) -> PagedResultOfApiAchievementDefinition:
        """achievements_get_all_achievements

        :param offset: offset, defaults to None
        :type offset: int, optional
        :param count: count, defaults to None
        :type count: int, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: PagedResultOfApiAchievementDefinition
        """

        Validator(int).is_optional().validate(offset)
        Validator(int).is_optional().validate(count)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/achievements", self.get_default_headers()
            )
            .add_query("offset", offset)
            .add_query("count", count)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return PagedResultOfApiAchievementDefinition._unmap(response)

    @cast_models
    def achievements_set_achievement(
        self, request_body: dict, contact_id: str, achievement_id: str
    ):
        """achievements_set_achievement

        :param request_body: The request body.
        :type request_body: dict
        :param contact_id: contact_id
        :type contact_id: str
        :param achievement_id: achievement_id
        :type achievement_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        """

        Validator(dict).validate(request_body)
        Validator(str).validate(contact_id)
        Validator(str).validate(achievement_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactId}}/achievements/{{achievementId}}",
                self.get_default_headers(),
            )
            .add_path("contactId", contact_id)
            .add_path("achievementId", achievement_id)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return response

    @cast_models
    def achievements_remove_achievement(self, contact_id: str, achievement_id: str):
        """achievements_remove_achievement

        :param contact_id: contact_id
        :type contact_id: str
        :param achievement_id: achievement_id
        :type achievement_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        """

        Validator(str).validate(contact_id)
        Validator(str).validate(achievement_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/contacts/{{contactId}}/achievements/{{achievementId}}",
                self.get_default_headers(),
            )
            .add_path("contactId", contact_id)
            .add_path("achievementId", achievement_id)
            .serialize()
            .set_method("DELETE")
        )

        response = self.send_request(serialized_request)

        return response
