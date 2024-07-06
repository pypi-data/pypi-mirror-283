from typing import List
from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.challenge_get_challenges_filter import ChallengeGetChallengesFilter
from ..models.challenge_get_challenge_definitions_status import (
    ChallengeGetChallengeDefinitionsStatus,
)
from ..models.challenge_definition_models_result import ChallengeDefinitionModelsResult
from ..models.challenge_definition_model import ChallengeDefinitionModel
from ..models.challenge_check_point_dto import ChallengeCheckPointDto
from ..models.challenge_assignment_models_result import ChallengeAssignmentModelsResult
from ..models.challenge_assignment_model import ChallengeAssignmentModel
from ..models.add_checkpoint_to_challenge_assignment_result import (
    AddCheckpointToChallengeAssignmentResult,
)


class ChallengesService(BaseService):

    @cast_models
    def challenge_get_challenge_by_id(self, id_: str) -> ChallengeAssignmentModel:
        """Get an challenge assignment by id.

        :param id_: Assignment id
        :type id_: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: ChallengeAssignmentModel
        """

        Validator(str).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/challenges/{{id}}", self.get_default_headers()
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return ChallengeAssignmentModel._unmap(response)

    @cast_models
    def challenge_get_challenge_definition_by_id(
        self, id_: str
    ) -> ChallengeDefinitionModel:
        """Get a challenge definition by id.

        :param id_: Definition id
        :type id_: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: ChallengeDefinitionModel
        """

        Validator(str).validate(id_)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/challenges/definitions/{{id}}",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return ChallengeDefinitionModel._unmap(response)

    @cast_models
    def challenge_get_challenge_definitions(
        self,
        offset: int = None,
        count: int = None,
        status: ChallengeGetChallengeDefinitionsStatus = None,
    ) -> ChallengeDefinitionModelsResult:
        """Get a list of all the challenge definitions.

        :param offset: Defaults to 0, defaults to None
        :type offset: int, optional
        :param count: Defaults to 100, defaults to None
        :type count: int, optional
        :param status: All, Active, Draft or Ended. If not specified it will default to All, defaults to None
        :type status: ChallengeGetChallengeDefinitionsStatus, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: ChallengeDefinitionModelsResult
        """

        Validator(int).is_optional().validate(offset)
        Validator(int).is_optional().validate(count)
        Validator(ChallengeGetChallengeDefinitionsStatus).is_optional().validate(status)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/challenges/definitions",
                self.get_default_headers(),
            )
            .add_query("offset", offset)
            .add_query("count", count)
            .add_query("status", status)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return ChallengeDefinitionModelsResult._unmap(response)

    @cast_models
    def challenge_get_challenges(
        self,
        contact_id: str,
        definition_id: str = None,
        offset: int = None,
        count: int = None,
        filter: ChallengeGetChallengesFilter = None,
    ) -> ChallengeAssignmentModelsResult:
        """Search for challenges for a contact.

        :param contact_id: Contact id
        :type contact_id: str
        :param definition_id: Definition id - Optional to limit to a certain challenge definition, defaults to None
        :type definition_id: str, optional
        :param offset: Defaults to 0, defaults to None
        :type offset: int, optional
        :param count: Defaults to 100, defaults to None
        :type count: int, optional
        :param filter: All, Active, Completed or NotCompleted. If not specified it will default to All, defaults to None
        :type filter: ChallengeGetChallengesFilter, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: ChallengeAssignmentModelsResult
        """

        Validator(str).validate(contact_id)
        Validator(str).is_optional().validate(definition_id)
        Validator(int).is_optional().validate(offset)
        Validator(int).is_optional().validate(count)
        Validator(ChallengeGetChallengesFilter).is_optional().validate(filter)

        serialized_request = (
            Serializer(f"{self.base_url}/api/v2/challenges", self.get_default_headers())
            .add_query("contactId", contact_id)
            .add_query("definitionId", definition_id)
            .add_query("offset", offset)
            .add_query("count", count)
            .add_query("filter", filter)
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)

        return ChallengeAssignmentModelsResult._unmap(response)

    @cast_models
    def challenge_add_challenge_check_points(
        self, request_body: List[ChallengeCheckPointDto]
    ) -> AddCheckpointToChallengeAssignmentResult:
        """Send in a list of checkpoints to be assigned to a some challenge for a number of contacts,
        the endpoint will able to take max 1000 checkpoint rows.

        ### The following fields should be provided:

        - definitionId: Must be a Guid
        - contactId: Must be a Guid
        - checkPointAmount: Number of checkpoints to assign to the challenge

        ### Important info:
        If some rows are not correct it will still result in an accepted response code and be skipped. Please
        check the response for NotAccepted items

        :param request_body: The request body.
        :type request_body: List[ChallengeCheckPointDto]
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: AddCheckpointToChallengeAssignmentResult
        """

        Validator(ChallengeCheckPointDto).is_array().validate(request_body)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/challenges/checkpoints",
                self.get_default_headers(),
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)

        return AddCheckpointToChallengeAssignmentResult._unmap(response)

    @cast_models
    def challenge_consent(self, id_: str, contact_id: str) -> bool:
        """Will assign the challenge for the contact and return true. If the contact already
        has been assigned for the challenge it will also return true.

        :param id_: Definition id
        :type id_: str
        :param contact_id: Contact id
        :type contact_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: bool
        """

        Validator(str).validate(id_)
        Validator(str).validate(contact_id)

        serialized_request = (
            Serializer(
                f"{self.base_url}/api/v2/challenges/definitions/{{id}}/assign",
                self.get_default_headers(),
            )
            .add_path("id", id_)
            .add_query("contactId", contact_id)
            .serialize()
            .set_method("POST")
        )

        response = self.send_request(serialized_request)

        return response
