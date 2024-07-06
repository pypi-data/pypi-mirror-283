from enum import Enum
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


class MultichannelPromotionRedemptionChannelModelType(Enum):
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
                MultichannelPromotionRedemptionChannelModelType._member_map_.values(),
            )
        )


class MultichannelPromotionRedemptionChannelModelValueType(Enum):
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
                MultichannelPromotionRedemptionChannelModelValueType._member_map_.values(),
            )
        )


@JsonMap({"type_": "type", "value_type": "valueType", "local_values": "localValues"})
class MultichannelPromotionRedemptionChannelModel(BaseModel):
    """MultichannelPromotionRedemptionChannelModel

    :param type_: type_, defaults to None
    :type type_: MultichannelPromotionRedemptionChannelModelType, optional
    :param value_type: value_type, defaults to None
    :type value_type: MultichannelPromotionRedemptionChannelModelValueType, optional
    :param value: The type of "Value" depends on "ValueType".
    <br>"MONEY" expects a decimal as a string ("20.5"). "SWIPE", "EXTERNALOFFER" and "MANUAL" expects a string ("Promotion"). "PERCENT" expects an integer as a string ("20")., defaults to None
    :type value: str, optional
    :param local_values: local_values, defaults to None
    :type local_values: List[dict], optional
    :param instruction: instruction, defaults to None
    :type instruction: str, optional
    """

    def __init__(
        self,
        type_: MultichannelPromotionRedemptionChannelModelType = None,
        value_type: MultichannelPromotionRedemptionChannelModelValueType = None,
        value: str = None,
        local_values: List[dict] = None,
        instruction: str = None,
    ):
        if type_ is not None:
            self.type_ = self._enum_matching(
                type_, MultichannelPromotionRedemptionChannelModelType.list(), "type_"
            )
        if value_type is not None:
            self.value_type = self._enum_matching(
                value_type,
                MultichannelPromotionRedemptionChannelModelValueType.list(),
                "value_type",
            )
        if value is not None:
            self.value = value
        if local_values is not None:
            self.local_values = local_values
        if instruction is not None:
            self.instruction = instruction
