from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .challenge_check_point_dto import ChallengeCheckPointDto


@JsonMap(
    {
        "missing_contact_ids": "missingContactIds",
        "missing_definition_ids": "missingDefinitionIds",
        "not_accepted": "notAccepted",
    }
)
class AddCheckpointToChallengeAssignmentResult(BaseModel):
    """AddCheckpointToChallengeAssignmentResult

    :param missing_contact_ids: missing_contact_ids, defaults to None
    :type missing_contact_ids: List[str], optional
    :param missing_definition_ids: missing_definition_ids, defaults to None
    :type missing_definition_ids: List[str], optional
    :param not_accepted: not_accepted, defaults to None
    :type not_accepted: List[ChallengeCheckPointDto], optional
    """

    def __init__(
        self,
        missing_contact_ids: List[str] = None,
        missing_definition_ids: List[str] = None,
        not_accepted: List[ChallengeCheckPointDto] = None,
    ):
        if missing_contact_ids is not None:
            self.missing_contact_ids = missing_contact_ids
        if missing_definition_ids is not None:
            self.missing_definition_ids = missing_definition_ids
        if not_accepted is not None:
            self.not_accepted = self._define_list(not_accepted, ChallengeCheckPointDto)
