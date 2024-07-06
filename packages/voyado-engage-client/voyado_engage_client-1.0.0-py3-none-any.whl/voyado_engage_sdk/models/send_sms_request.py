from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"invoice_reference": "invoiceReference", "phone_numbers": "phoneNumbers"})
class SendSmsRequest(BaseModel):
    """SendSmsRequest

    :param description: description, defaults to None
    :type description: str, optional
    :param invoice_reference: invoice_reference, defaults to None
    :type invoice_reference: str, optional
    :param message: message, defaults to None
    :type message: str, optional
    :param phone_numbers: phone_numbers, defaults to None
    :type phone_numbers: List[str], optional
    :param sender: sender, defaults to None
    :type sender: str, optional
    """

    def __init__(
        self,
        description: str = None,
        invoice_reference: str = None,
        message: str = None,
        phone_numbers: List[str] = None,
        sender: str = None,
    ):
        if description is not None:
            self.description = description
        if invoice_reference is not None:
            self.invoice_reference = invoice_reference
        if message is not None:
            self.message = message
        if phone_numbers is not None:
            self.phone_numbers = phone_numbers
        if sender is not None:
            self.sender = sender
