from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"type_": "type", "extra_data": "extraData"})
class OrderPaymentMethod(BaseModel):
    """OrderPaymentMethod

    :param type_: type_
    :type type_: str
    :param description: description, defaults to None
    :type description: str, optional
    :param value: value
    :type value: float
    :param extra_data: extra_data, defaults to None
    :type extra_data: dict, optional
    """

    def __init__(
        self, type_: str, value: float, description: str = None, extra_data: dict = None
    ):
        self.type_ = type_
        if description is not None:
            self.description = description
        self.value = value
        if extra_data is not None:
            self.extra_data = extra_data
