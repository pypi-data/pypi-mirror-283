from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap(
    {
        "id_": "id",
        "transaction_number": "transactionNumber",
        "created_date": "createdDate",
        "store_name": "storeName",
        "number_of_items": "numberOfItems",
        "net_price_sum": "netPriceSum",
        "local_net_price_sum": "localNetPriceSum",
        "local_currency": "localCurrency",
        "group_currency": "groupCurrency",
        "store_type": "storeType",
        "line_items": "lineItems",
        "external_id": "externalId",
    }
)
class TransactionItem(BaseModel):
    """TransactionItem

    :param id_: id_, defaults to None
    :type id_: str, optional
    :param transaction_number: transaction_number, defaults to None
    :type transaction_number: str, optional
    :param created_date: created_date, defaults to None
    :type created_date: str, optional
    :param store_name: store_name, defaults to None
    :type store_name: str, optional
    :param number_of_items: number_of_items, defaults to None
    :type number_of_items: int, optional
    :param net_price_sum: net_price_sum, defaults to None
    :type net_price_sum: float, optional
    :param local_net_price_sum: local_net_price_sum, defaults to None
    :type local_net_price_sum: float, optional
    :param local_currency: local_currency, defaults to None
    :type local_currency: str, optional
    :param group_currency: group_currency, defaults to None
    :type group_currency: str, optional
    :param store_type: store_type, defaults to None
    :type store_type: str, optional
    :param line_items: line_items, defaults to None
    :type line_items: List[dict], optional
    :param external_id: external_id, defaults to None
    :type external_id: str, optional
    """

    def __init__(
        self,
        id_: str = None,
        transaction_number: str = None,
        created_date: str = None,
        store_name: str = None,
        number_of_items: int = None,
        net_price_sum: float = None,
        local_net_price_sum: float = None,
        local_currency: str = None,
        group_currency: str = None,
        store_type: str = None,
        line_items: List[dict] = None,
        external_id: str = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if transaction_number is not None:
            self.transaction_number = transaction_number
        if created_date is not None:
            self.created_date = created_date
        if store_name is not None:
            self.store_name = store_name
        if number_of_items is not None:
            self.number_of_items = number_of_items
        if net_price_sum is not None:
            self.net_price_sum = net_price_sum
        if local_net_price_sum is not None:
            self.local_net_price_sum = local_net_price_sum
        if local_currency is not None:
            self.local_currency = local_currency
        if group_currency is not None:
            self.group_currency = group_currency
        if store_type is not None:
            self.store_type = store_type
        if line_items is not None:
            self.line_items = line_items
        if external_id is not None:
            self.external_id = external_id
