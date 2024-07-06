from enum import Enum
from .utils.json_map import JsonMap
from .base import BaseModel


class BonusPointTransactionModelType(Enum):
    """An enumeration representing different categories.

    :cvar PURCHASE: "Purchase"
    :vartype PURCHASE: str
    :cvar ADJUSTMENT: "Adjustment"
    :vartype ADJUSTMENT: str
    :cvar RECRUITMENT: "Recruitment"
    :vartype RECRUITMENT: str
    :cvar PURCHASEREDUCTION: "PurchaseReduction"
    :vartype PURCHASEREDUCTION: str
    :cvar RETURN: "Return"
    :vartype RETURN: str
    :cvar BONUSCHECK: "BonusCheck"
    :vartype BONUSCHECK: str
    :cvar DUEDATE: "DueDate"
    :vartype DUEDATE: str
    :cvar STARTBONUS: "StartBonus"
    :vartype STARTBONUS: str
    :cvar BONUSPROMOTION: "BonusPromotion"
    :vartype BONUSPROMOTION: str
    :cvar BONUSPROMOTIONRETURN: "BonusPromotionReturn"
    :vartype BONUSPROMOTIONRETURN: str
    :cvar FROMAUTOMATION: "FromAutomation"
    :vartype FROMAUTOMATION: str
    :cvar BONUSBALANCEADJUSTMENT: "BonusBalanceAdjustment"
    :vartype BONUSBALANCEADJUSTMENT: str
    :cvar PURCHASEWITHPOINTS: "PurchaseWithPoints"
    :vartype PURCHASEWITHPOINTS: str
    """

    PURCHASE = "Purchase"
    ADJUSTMENT = "Adjustment"
    RECRUITMENT = "Recruitment"
    PURCHASEREDUCTION = "PurchaseReduction"
    RETURN = "Return"
    BONUSCHECK = "BonusCheck"
    DUEDATE = "DueDate"
    STARTBONUS = "StartBonus"
    BONUSPROMOTION = "BonusPromotion"
    BONUSPROMOTIONRETURN = "BonusPromotionReturn"
    FROMAUTOMATION = "FromAutomation"
    BONUSBALANCEADJUSTMENT = "BonusBalanceAdjustment"
    PURCHASEWITHPOINTS = "PurchaseWithPoints"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, BonusPointTransactionModelType._member_map_.values())
        )


@JsonMap(
    {
        "transaction_date_time": "transactionDateTime",
        "type_": "type",
        "id_": "id",
        "automation_bonus_adjustment_reason": "automationBonusAdjustmentReason",
    }
)
class BonusPointTransactionModel(BaseModel):
    """BonusPointTransactionModel

    :param amount: amount, defaults to None
    :type amount: float, optional
    :param transaction_date_time: transaction_date_time, defaults to None
    :type transaction_date_time: str, optional
    :param description: description, defaults to None
    :type description: str, optional
    :param type_: type_, defaults to None
    :type type_: BonusPointTransactionModelType, optional
    :param id_: id_, defaults to None
    :type id_: str, optional
    :param automation_bonus_adjustment_reason: automation_bonus_adjustment_reason, defaults to None
    :type automation_bonus_adjustment_reason: str, optional
    """

    def __init__(
        self,
        amount: float = None,
        transaction_date_time: str = None,
        description: str = None,
        type_: BonusPointTransactionModelType = None,
        id_: str = None,
        automation_bonus_adjustment_reason: str = None,
    ):
        if amount is not None:
            self.amount = amount
        if transaction_date_time is not None:
            self.transaction_date_time = transaction_date_time
        if description is not None:
            self.description = description
        if type_ is not None:
            self.type_ = self._enum_matching(
                type_, BonusPointTransactionModelType.list(), "type_"
            )
        if id_ is not None:
            self.id_ = id_
        if automation_bonus_adjustment_reason is not None:
            self.automation_bonus_adjustment_reason = automation_bonus_adjustment_reason
