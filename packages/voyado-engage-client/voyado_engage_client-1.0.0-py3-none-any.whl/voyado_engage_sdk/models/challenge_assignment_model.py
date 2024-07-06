from __future__ import annotations
from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .i_hypermedia_link import IHypermediaLink


class ChallengeAssignmentModelStatus(Enum):
    """An enumeration representing different categories.

    :cvar UNKNOWN: "Unknown"
    :vartype UNKNOWN: str
    :cvar COMPLETED: "Completed"
    :vartype COMPLETED: str
    :cvar NOTCOMPLETED: "NotCompleted"
    :vartype NOTCOMPLETED: str
    :cvar ACTIVE: "Active"
    :vartype ACTIVE: str
    """

    UNKNOWN = "Unknown"
    COMPLETED = "Completed"
    NOTCOMPLETED = "NotCompleted"
    ACTIVE = "Active"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, ChallengeAssignmentModelStatus._member_map_.values())
        )


@JsonMap(
    {
        "challenge_completed_on": "challengeCompletedOn",
        "challenge_end": "challengeEnd",
        "challenge_id": "challengeId",
        "challenge_start": "challengeStart",
        "completed_checkpoints": "completedCheckpoints",
        "image_url": "imageUrl",
        "contact_id": "contactId",
        "id_": "id",
        "is_active": "isActive",
        "is_challenge_completed": "isChallengeCompleted",
        "latest_checkpoint_added_on": "latestCheckpointAddedOn",
        "required_checkpoints": "requiredCheckpoints",
    }
)
class ChallengeAssignmentModel(BaseModel):
    """ChallengeAssignmentModel

    :param challenge_completed_on: challenge_completed_on, defaults to None
    :type challenge_completed_on: str, optional
    :param challenge_end: challenge_end, defaults to None
    :type challenge_end: str, optional
    :param challenge_id: challenge_id, defaults to None
    :type challenge_id: str, optional
    :param challenge_start: challenge_start, defaults to None
    :type challenge_start: str, optional
    :param completed_checkpoints: completed_checkpoints, defaults to None
    :type completed_checkpoints: int, optional
    :param image_url: image_url, defaults to None
    :type image_url: str, optional
    :param contact_id: contact_id, defaults to None
    :type contact_id: str, optional
    :param id_: id_, defaults to None
    :type id_: str, optional
    :param is_active: is_active, defaults to None
    :type is_active: bool, optional
    :param is_challenge_completed: is_challenge_completed, defaults to None
    :type is_challenge_completed: bool, optional
    :param latest_checkpoint_added_on: latest_checkpoint_added_on, defaults to None
    :type latest_checkpoint_added_on: str, optional
    :param required_checkpoints: required_checkpoints, defaults to None
    :type required_checkpoints: int, optional
    :param status: status, defaults to None
    :type status: ChallengeAssignmentModelStatus, optional
    :param links: links, defaults to None
    :type links: List[IHypermediaLink], optional
    """

    def __init__(
        self,
        challenge_completed_on: str = None,
        challenge_end: str = None,
        challenge_id: str = None,
        challenge_start: str = None,
        completed_checkpoints: int = None,
        image_url: str = None,
        contact_id: str = None,
        id_: str = None,
        is_active: bool = None,
        is_challenge_completed: bool = None,
        latest_checkpoint_added_on: str = None,
        required_checkpoints: int = None,
        status: ChallengeAssignmentModelStatus = None,
        links: List[IHypermediaLink] = None,
    ):
        if challenge_completed_on is not None:
            self.challenge_completed_on = challenge_completed_on
        if challenge_end is not None:
            self.challenge_end = challenge_end
        if challenge_id is not None:
            self.challenge_id = challenge_id
        if challenge_start is not None:
            self.challenge_start = challenge_start
        if completed_checkpoints is not None:
            self.completed_checkpoints = completed_checkpoints
        if image_url is not None:
            self.image_url = image_url
        if contact_id is not None:
            self.contact_id = contact_id
        if id_ is not None:
            self.id_ = id_
        if is_active is not None:
            self.is_active = is_active
        if is_challenge_completed is not None:
            self.is_challenge_completed = is_challenge_completed
        if latest_checkpoint_added_on is not None:
            self.latest_checkpoint_added_on = latest_checkpoint_added_on
        if required_checkpoints is not None:
            self.required_checkpoints = required_checkpoints
        if status is not None:
            self.status = self._enum_matching(
                status, ChallengeAssignmentModelStatus.list(), "status"
            )
        if links is not None:
            self.links = self._define_list(links, IHypermediaLink)
