from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .receipt_contact import ReceiptContact
from .receipt_tax_detail import ReceiptTaxDetail
from .receipt_payment_method import ReceiptPaymentMethod
from .receipt_item import ReceiptItem
from .receipt_used_bonus_check import ReceiptUsedBonusCheck
from .receipt_used_promotion import ReceiptUsedPromotion
from .receipt_extra_data_item import ReceiptExtraDataItem


@JsonMap(
    {
        "unique_receipt_id": "uniqueReceiptId",
        "receipt_number": "receiptNumber",
        "created_date": "createdDate",
        "store_external_id": "storeExternalId",
        "exchange_rate_to_group_currency": "exchangeRateToGroupCurrency",
        "total_gross_price": "totalGrossPrice",
        "tax_details": "taxDetails",
        "payment_methods": "paymentMethods",
        "used_bonus_checks": "usedBonusChecks",
        "used_promotions": "usedPromotions",
        "extra_data": "extraData",
    }
)
class Receipt(BaseModel):
    """Receipt

    :param contact: contact
    :type contact: ReceiptContact
    :param unique_receipt_id: unique_receipt_id
    :type unique_receipt_id: str
    :param receipt_number: receipt_number
    :type receipt_number: str
    :param created_date: created_date
    :type created_date: str
    :param store_external_id: store_external_id
    :type store_external_id: str
    :param currency: currency
    :type currency: str
    :param exchange_rate_to_group_currency: exchange_rate_to_group_currency, defaults to None
    :type exchange_rate_to_group_currency: float, optional
    :param total_gross_price: total_gross_price
    :type total_gross_price: float
    :param tax_details: tax_details, defaults to None
    :type tax_details: List[ReceiptTaxDetail], optional
    :param payment_methods: payment_methods
    :type payment_methods: List[ReceiptPaymentMethod]
    :param items: items
    :type items: List[ReceiptItem]
    :param used_bonus_checks: used_bonus_checks, defaults to None
    :type used_bonus_checks: List[ReceiptUsedBonusCheck], optional
    :param used_promotions: used_promotions, defaults to None
    :type used_promotions: List[ReceiptUsedPromotion], optional
    :param extra_data: extra_data, defaults to None
    :type extra_data: List[ReceiptExtraDataItem], optional
    """

    def __init__(
        self,
        contact: ReceiptContact,
        unique_receipt_id: str,
        receipt_number: str,
        created_date: str,
        store_external_id: str,
        currency: str,
        total_gross_price: float,
        payment_methods: List[ReceiptPaymentMethod],
        items: List[ReceiptItem],
        exchange_rate_to_group_currency: float = None,
        tax_details: List[ReceiptTaxDetail] = None,
        used_bonus_checks: List[ReceiptUsedBonusCheck] = None,
        used_promotions: List[ReceiptUsedPromotion] = None,
        extra_data: List[ReceiptExtraDataItem] = None,
    ):
        self.contact = self._define_object(contact, ReceiptContact)
        self.unique_receipt_id = unique_receipt_id
        self.receipt_number = receipt_number
        self.created_date = created_date
        self.store_external_id = store_external_id
        self.currency = currency
        if exchange_rate_to_group_currency is not None:
            self.exchange_rate_to_group_currency = exchange_rate_to_group_currency
        self.total_gross_price = total_gross_price
        if tax_details is not None:
            self.tax_details = self._define_list(tax_details, ReceiptTaxDetail)
        self.payment_methods = self._define_list(payment_methods, ReceiptPaymentMethod)
        self.items = self._define_list(items, ReceiptItem)
        if used_bonus_checks is not None:
            self.used_bonus_checks = self._define_list(
                used_bonus_checks, ReceiptUsedBonusCheck
            )
        if used_promotions is not None:
            self.used_promotions = self._define_list(
                used_promotions, ReceiptUsedPromotion
            )
        if extra_data is not None:
            self.extra_data = self._define_list(extra_data, ReceiptExtraDataItem)
