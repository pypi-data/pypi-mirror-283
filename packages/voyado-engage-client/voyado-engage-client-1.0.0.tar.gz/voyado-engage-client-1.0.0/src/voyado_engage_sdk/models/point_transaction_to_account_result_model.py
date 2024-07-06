from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .point_transaction_to_account import PointTransactionToAccount


@JsonMap(
    {
        "not_accepted": "notAccepted",
        "error_messages": "errorMessages",
        "missing_definition_ids": "missingDefinitionIds",
        "missing_contact_ids": "missingContactIds",
    }
)
class PointTransactionToAccountResultModel(BaseModel):
    """PointTransactionToAccountResultModel

    :param not_accepted: not_accepted, defaults to None
    :type not_accepted: List[PointTransactionToAccount], optional
    :param error_messages: error_messages, defaults to None
    :type error_messages: List[str], optional
    :param missing_definition_ids: missing_definition_ids, defaults to None
    :type missing_definition_ids: List[int], optional
    :param missing_contact_ids: missing_contact_ids, defaults to None
    :type missing_contact_ids: List[str], optional
    """

    def __init__(
        self,
        not_accepted: List[PointTransactionToAccount] = None,
        error_messages: List[str] = None,
        missing_definition_ids: List[int] = None,
        missing_contact_ids: List[str] = None,
    ):
        if not_accepted is not None:
            self.not_accepted = self._define_list(
                not_accepted, PointTransactionToAccount
            )
        if error_messages is not None:
            self.error_messages = error_messages
        if missing_definition_ids is not None:
            self.missing_definition_ids = missing_definition_ids
        if missing_contact_ids is not None:
            self.missing_contact_ids = missing_contact_ids
