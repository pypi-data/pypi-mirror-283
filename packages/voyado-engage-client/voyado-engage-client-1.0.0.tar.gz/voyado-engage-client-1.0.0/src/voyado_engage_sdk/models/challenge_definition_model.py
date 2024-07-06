from __future__ import annotations
from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .i_hypermedia_link import IHypermediaLink


class CheckpointAssignOn(Enum):
    """An enumeration representing different categories.

    :cvar NONE: "None"
    :vartype NONE: str
    :cvar RECEIPTTOTAL: "ReceiptTotal"
    :vartype RECEIPTTOTAL: str
    :cvar RECEIPTLINEQUANTITY: "ReceiptLineQuantity"
    :vartype RECEIPTLINEQUANTITY: str
    :cvar RECEIPTLINETOTAL: "ReceiptLineTotal"
    :vartype RECEIPTLINETOTAL: str
    """

    NONE = "None"
    RECEIPTTOTAL = "ReceiptTotal"
    RECEIPTLINEQUANTITY = "ReceiptLineQuantity"
    RECEIPTLINETOTAL = "ReceiptLineTotal"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, CheckpointAssignOn._member_map_.values()))


class ChallengeDefinitionModelStatus(Enum):
    """An enumeration representing different categories.

    :cvar ALL: "All"
    :vartype ALL: str
    :cvar ACTIVE: "Active"
    :vartype ACTIVE: str
    :cvar DRAFT: "Draft"
    :vartype DRAFT: str
    :cvar SCHEDULED: "Scheduled"
    :vartype SCHEDULED: str
    :cvar ENDED: "Ended"
    :vartype ENDED: str
    """

    ALL = "All"
    ACTIVE = "Active"
    DRAFT = "Draft"
    SCHEDULED = "Scheduled"
    ENDED = "Ended"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, ChallengeDefinitionModelStatus._member_map_.values())
        )


@JsonMap(
    {
        "checkpoint_assign_on": "checkpointAssignOn",
        "checkpoint_assign_on_amount": "checkpointAssignOnAmount",
        "created_by": "createdBy",
        "created_on": "createdOn",
        "expiration_months": "expirationMonths",
        "id_": "id",
        "is_contact_consent_required": "isContactConsentRequired",
        "is_scheduled": "isScheduled",
        "modified_by": "modifiedBy",
        "modified_on": "modifiedOn",
        "required_number_of_checkpoints": "requiredNumberOfCheckpoints",
        "scheduled_from": "scheduledFrom",
        "scheduled_to": "scheduledTo",
    }
)
class ChallengeDefinitionModel(BaseModel):
    """ChallengeDefinitionModel

    :param checkpoint_assign_on: checkpoint_assign_on, defaults to None
    :type checkpoint_assign_on: CheckpointAssignOn, optional
    :param checkpoint_assign_on_amount: checkpoint_assign_on_amount, defaults to None
    :type checkpoint_assign_on_amount: float, optional
    :param created_by: created_by, defaults to None
    :type created_by: str, optional
    :param created_on: created_on, defaults to None
    :type created_on: str, optional
    :param description: description, defaults to None
    :type description: str, optional
    :param expiration_months: expiration_months, defaults to None
    :type expiration_months: int, optional
    :param id_: id_, defaults to None
    :type id_: str, optional
    :param is_contact_consent_required: is_contact_consent_required, defaults to None
    :type is_contact_consent_required: bool, optional
    :param is_scheduled: is_scheduled, defaults to None
    :type is_scheduled: bool, optional
    :param modified_by: modified_by, defaults to None
    :type modified_by: str, optional
    :param modified_on: modified_on, defaults to None
    :type modified_on: str, optional
    :param name: name, defaults to None
    :type name: str, optional
    :param required_number_of_checkpoints: required_number_of_checkpoints, defaults to None
    :type required_number_of_checkpoints: int, optional
    :param scheduled_from: scheduled_from, defaults to None
    :type scheduled_from: str, optional
    :param scheduled_to: scheduled_to, defaults to None
    :type scheduled_to: str, optional
    :param status: status, defaults to None
    :type status: ChallengeDefinitionModelStatus, optional
    :param links: links, defaults to None
    :type links: List[IHypermediaLink], optional
    """

    def __init__(
        self,
        checkpoint_assign_on: CheckpointAssignOn = None,
        checkpoint_assign_on_amount: float = None,
        created_by: str = None,
        created_on: str = None,
        description: str = None,
        expiration_months: int = None,
        id_: str = None,
        is_contact_consent_required: bool = None,
        is_scheduled: bool = None,
        modified_by: str = None,
        modified_on: str = None,
        name: str = None,
        required_number_of_checkpoints: int = None,
        scheduled_from: str = None,
        scheduled_to: str = None,
        status: ChallengeDefinitionModelStatus = None,
        links: List[IHypermediaLink] = None,
    ):
        if checkpoint_assign_on is not None:
            self.checkpoint_assign_on = self._enum_matching(
                checkpoint_assign_on, CheckpointAssignOn.list(), "checkpoint_assign_on"
            )
        if checkpoint_assign_on_amount is not None:
            self.checkpoint_assign_on_amount = checkpoint_assign_on_amount
        if created_by is not None:
            self.created_by = created_by
        if created_on is not None:
            self.created_on = created_on
        if description is not None:
            self.description = description
        if expiration_months is not None:
            self.expiration_months = expiration_months
        if id_ is not None:
            self.id_ = id_
        if is_contact_consent_required is not None:
            self.is_contact_consent_required = is_contact_consent_required
        if is_scheduled is not None:
            self.is_scheduled = is_scheduled
        if modified_by is not None:
            self.modified_by = modified_by
        if modified_on is not None:
            self.modified_on = modified_on
        if name is not None:
            self.name = name
        if required_number_of_checkpoints is not None:
            self.required_number_of_checkpoints = required_number_of_checkpoints
        if scheduled_from is not None:
            self.scheduled_from = scheduled_from
        if scheduled_to is not None:
            self.scheduled_to = scheduled_to
        if status is not None:
            self.status = self._enum_matching(
                status, ChallengeDefinitionModelStatus.list(), "status"
            )
        if links is not None:
            self.links = self._define_list(links, IHypermediaLink)
