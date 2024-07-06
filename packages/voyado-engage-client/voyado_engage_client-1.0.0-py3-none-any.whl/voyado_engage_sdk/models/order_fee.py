from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"tax_percent": "taxPercent"})
class OrderFee(BaseModel):
    """OrderFee

    :param value: value
    :type value: float
    :param tax: tax, defaults to None
    :type tax: float, optional
    :param tax_percent: tax_percent, defaults to None
    :type tax_percent: float, optional
    """

    def __init__(self, value: float, tax: float = None, tax_percent: float = None):
        self.value = value
        if tax is not None:
            self.tax = tax
        if tax_percent is not None:
            self.tax_percent = tax_percent
