from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .order_contact import OrderContact
from .tax_detail import TaxDetail
from .order_payment_method import OrderPaymentMethod
from .order_item import OrderItem
from .order_fee import OrderFee


@JsonMap(
    {
        "order_number": "orderNumber",
        "order_status": "orderStatus",
        "payment_status": "paymentStatus",
        "created_date": "createdDate",
        "shipping_date": "shippingDate",
        "status_changed_date": "statusChangedDate",
        "store_id": "storeId",
        "exchange_rate_to_group_currency": "exchangeRateToGroupCurrency",
        "extra_data": "extraData",
        "total_gross_price": "totalGrossPrice",
        "total_tax": "totalTax",
        "tax_details": "taxDetails",
        "payment_methods": "paymentMethods",
        "freight_fee": "freightFee",
        "handling_fee": "handlingFee",
        "total_round_off": "totalRoundOff",
        "total_discounts": "totalDiscounts",
        "total_original_price": "totalOriginalPrice",
        "total_items_price": "totalItemsPrice",
        "total_net_price": "totalNetPrice",
        "any_return_items": "anyReturnItems",
    }
)
class Order(BaseModel):
    """Order

    :param contact: contact
    :type contact: OrderContact
    :param order_number: order_number
    :type order_number: str
    :param order_status: order_status
    :type order_status: str
    :param payment_status: payment_status
    :type payment_status: str
    :param language: language, defaults to None
    :type language: str, optional
    :param created_date: created_date
    :type created_date: str
    :param shipping_date: shipping_date, defaults to None
    :type shipping_date: str, optional
    :param status_changed_date: status_changed_date, defaults to None
    :type status_changed_date: str, optional
    :param store_id: store_id
    :type store_id: str
    :param currency: currency
    :type currency: str
    :param exchange_rate_to_group_currency: exchange_rate_to_group_currency, defaults to None
    :type exchange_rate_to_group_currency: float, optional
    :param extra_data: extra_data, defaults to None
    :type extra_data: dict, optional
    :param total_gross_price: total_gross_price
    :type total_gross_price: float
    :param total_tax: total_tax, defaults to None
    :type total_tax: float, optional
    :param tax_details: tax_details, defaults to None
    :type tax_details: List[TaxDetail], optional
    :param payment_methods: payment_methods, defaults to None
    :type payment_methods: List[OrderPaymentMethod], optional
    :param items: items
    :type items: List[OrderItem]
    :param freight_fee: freight_fee, defaults to None
    :type freight_fee: OrderFee, optional
    :param handling_fee: handling_fee, defaults to None
    :type handling_fee: OrderFee, optional
    :param total_round_off: total_round_off, defaults to None
    :type total_round_off: OrderFee, optional
    :param total_discounts: total_discounts, defaults to None
    :type total_discounts: float, optional
    :param total_original_price: total_original_price, defaults to None
    :type total_original_price: float, optional
    :param total_items_price: total_items_price, defaults to None
    :type total_items_price: float, optional
    :param total_net_price: total_net_price, defaults to None
    :type total_net_price: float, optional
    :param any_return_items: any_return_items, defaults to None
    :type any_return_items: bool, optional
    """

    def __init__(
        self,
        contact: OrderContact,
        order_number: str,
        order_status: str,
        payment_status: str,
        created_date: str,
        store_id: str,
        currency: str,
        total_gross_price: float,
        items: List[OrderItem],
        language: str = None,
        shipping_date: str = None,
        status_changed_date: str = None,
        exchange_rate_to_group_currency: float = None,
        extra_data: dict = None,
        total_tax: float = None,
        tax_details: List[TaxDetail] = None,
        payment_methods: List[OrderPaymentMethod] = None,
        freight_fee: OrderFee = None,
        handling_fee: OrderFee = None,
        total_round_off: OrderFee = None,
        total_discounts: float = None,
        total_original_price: float = None,
        total_items_price: float = None,
        total_net_price: float = None,
        any_return_items: bool = None,
    ):
        self.contact = self._define_object(contact, OrderContact)
        self.order_number = order_number
        self.order_status = order_status
        self.payment_status = payment_status
        if language is not None:
            self.language = language
        self.created_date = created_date
        if shipping_date is not None:
            self.shipping_date = shipping_date
        if status_changed_date is not None:
            self.status_changed_date = status_changed_date
        self.store_id = store_id
        self.currency = currency
        if exchange_rate_to_group_currency is not None:
            self.exchange_rate_to_group_currency = exchange_rate_to_group_currency
        if extra_data is not None:
            self.extra_data = extra_data
        self.total_gross_price = total_gross_price
        if total_tax is not None:
            self.total_tax = total_tax
        if tax_details is not None:
            self.tax_details = self._define_list(tax_details, TaxDetail)
        if payment_methods is not None:
            self.payment_methods = self._define_list(
                payment_methods, OrderPaymentMethod
            )
        self.items = self._define_list(items, OrderItem)
        if freight_fee is not None:
            self.freight_fee = self._define_object(freight_fee, OrderFee)
        if handling_fee is not None:
            self.handling_fee = self._define_object(handling_fee, OrderFee)
        if total_round_off is not None:
            self.total_round_off = self._define_object(total_round_off, OrderFee)
        if total_discounts is not None:
            self.total_discounts = total_discounts
        if total_original_price is not None:
            self.total_original_price = total_original_price
        if total_items_price is not None:
            self.total_items_price = total_items_price
        if total_net_price is not None:
            self.total_net_price = total_net_price
        if any_return_items is not None:
            self.any_return_items = any_return_items
