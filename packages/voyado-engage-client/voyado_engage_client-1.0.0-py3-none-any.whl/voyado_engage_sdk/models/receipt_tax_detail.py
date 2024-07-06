from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap(
    {
        "total_including_tax": "totalIncludingTax",
        "total_excluding_tax": "totalExcludingTax",
    }
)
class ReceiptTaxDetail(BaseModel):
    """ReceiptTaxDetail

    :param description: description, defaults to None
    :type description: str, optional
    :param value: value, defaults to None
    :type value: float, optional
    :param percent: percent, defaults to None
    :type percent: float, optional
    :param total_including_tax: total_including_tax, defaults to None
    :type total_including_tax: float, optional
    :param total_excluding_tax: total_excluding_tax, defaults to None
    :type total_excluding_tax: float, optional
    """

    def __init__(
        self,
        description: str = None,
        value: float = None,
        percent: float = None,
        total_including_tax: float = None,
        total_excluding_tax: float = None,
    ):
        if description is not None:
            self.description = description
        if value is not None:
            self.value = value
        if percent is not None:
            self.percent = percent
        if total_including_tax is not None:
            self.total_including_tax = total_including_tax
        if total_excluding_tax is not None:
            self.total_excluding_tax = total_excluding_tax
