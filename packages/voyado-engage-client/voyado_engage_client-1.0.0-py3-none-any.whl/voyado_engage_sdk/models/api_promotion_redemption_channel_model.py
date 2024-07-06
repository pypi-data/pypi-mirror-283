from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


class ApiPromotionRedemptionChannelModelType(Enum):
    """An enumeration representing different categories.

    :cvar POS: "POS"
    :vartype POS: str
    :cvar ECOM: "ECOM"
    :vartype ECOM: str
    :cvar OTHER: "OTHER"
    :vartype OTHER: str
    """

    POS = "POS"
    ECOM = "ECOM"
    OTHER = "OTHER"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(
                lambda x: x.value,
                ApiPromotionRedemptionChannelModelType._member_map_.values(),
            )
        )


class ApiPromotionRedemptionChannelModelValueType(Enum):
    """An enumeration representing different categories.

    :cvar PERCENT: "PERCENT"
    :vartype PERCENT: str
    :cvar MONEY: "MONEY"
    :vartype MONEY: str
    :cvar EXTERNALOFFER: "EXTERNALOFFER"
    :vartype EXTERNALOFFER: str
    :cvar MANUAL: "MANUAL"
    :vartype MANUAL: str
    :cvar SWIPE: "SWIPE"
    :vartype SWIPE: str
    """

    PERCENT = "PERCENT"
    MONEY = "MONEY"
    EXTERNALOFFER = "EXTERNALOFFER"
    MANUAL = "MANUAL"
    SWIPE = "SWIPE"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(
                lambda x: x.value,
                ApiPromotionRedemptionChannelModelValueType._member_map_.values(),
            )
        )


@JsonMap({"type_": "type", "value_type": "valueType", "local_values": "localValues"})
class ApiPromotionRedemptionChannelModel(BaseModel):
    """ApiPromotionRedemptionChannelModel

    :param type_: type_, defaults to None
    :type type_: ApiPromotionRedemptionChannelModelType, optional
    :param value_type: value_type, defaults to None
    :type value_type: ApiPromotionRedemptionChannelModelValueType, optional
    :param value: The type of "Value" depends on "ValueType".
    <br>"MONEY" returns a Money object (Amount+Currency), "EXTERNALOFFER" and "MANUAL" returns a string ("Promotion"). "PERCENT" returns an integer., defaults to None
    :type value: any, optional
    :param local_values: local_values, defaults to None
    :type local_values: List[dict], optional
    :param instruction: instruction, defaults to None
    :type instruction: str, optional
    """

    def __init__(
        self,
        type_: ApiPromotionRedemptionChannelModelType = None,
        value_type: ApiPromotionRedemptionChannelModelValueType = None,
        value: any = None,
        local_values: List[dict] = None,
        instruction: str = None,
    ):
        if type_ is not None:
            self.type_ = self._enum_matching(
                type_, ApiPromotionRedemptionChannelModelType.list(), "type_"
            )
        if value_type is not None:
            self.value_type = self._enum_matching(
                value_type,
                ApiPromotionRedemptionChannelModelValueType.list(),
                "value_type",
            )
        if value is not None:
            self.value = value
        if local_values is not None:
            self.local_values = local_values
        if instruction is not None:
            self.instruction = instruction
