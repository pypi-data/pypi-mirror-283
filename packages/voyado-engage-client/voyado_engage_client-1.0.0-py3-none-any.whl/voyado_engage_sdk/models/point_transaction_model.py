from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .i_hypermedia_link import IHypermediaLink


@JsonMap(
    {
        "account_id": "accountId",
        "created_on": "createdOn",
        "id_": "id",
        "modified_on": "modifiedOn",
        "transaction_date": "transactionDate",
        "type_": "type",
        "valid_from": "validFrom",
        "valid_to": "validTo",
        "retail_transaction_line_item_id": "retailTransactionLineItemId",
    }
)
class PointTransactionModel(BaseModel):
    """PointTransactionModel

    :param account_id: account_id, defaults to None
    :type account_id: int, optional
    :param amount: amount, defaults to None
    :type amount: float, optional
    :param created_on: created_on, defaults to None
    :type created_on: str, optional
    :param description: description, defaults to None
    :type description: str, optional
    :param id_: id_, defaults to None
    :type id_: int, optional
    :param modified_on: modified_on, defaults to None
    :type modified_on: str, optional
    :param source: source, defaults to None
    :type source: str, optional
    :param transaction_date: transaction_date, defaults to None
    :type transaction_date: str, optional
    :param type_: type_, defaults to None
    :type type_: str, optional
    :param valid_from: valid_from, defaults to None
    :type valid_from: str, optional
    :param valid_to: valid_to, defaults to None
    :type valid_to: str, optional
    :param retail_transaction_line_item_id: retail_transaction_line_item_id, defaults to None
    :type retail_transaction_line_item_id: str, optional
    :param links: links, defaults to None
    :type links: List[IHypermediaLink], optional
    """

    def __init__(
        self,
        account_id: int = None,
        amount: float = None,
        created_on: str = None,
        description: str = None,
        id_: int = None,
        modified_on: str = None,
        source: str = None,
        transaction_date: str = None,
        type_: str = None,
        valid_from: str = None,
        valid_to: str = None,
        retail_transaction_line_item_id: str = None,
        links: List[IHypermediaLink] = None,
    ):
        if account_id is not None:
            self.account_id = account_id
        if amount is not None:
            self.amount = amount
        if created_on is not None:
            self.created_on = created_on
        if description is not None:
            self.description = description
        if id_ is not None:
            self.id_ = id_
        if modified_on is not None:
            self.modified_on = modified_on
        if source is not None:
            self.source = source
        if transaction_date is not None:
            self.transaction_date = transaction_date
        if type_ is not None:
            self.type_ = type_
        if valid_from is not None:
            self.valid_from = valid_from
        if valid_to is not None:
            self.valid_to = valid_to
        if retail_transaction_line_item_id is not None:
            self.retail_transaction_line_item_id = retail_transaction_line_item_id
        if links is not None:
            self.links = self._define_list(links, IHypermediaLink)
