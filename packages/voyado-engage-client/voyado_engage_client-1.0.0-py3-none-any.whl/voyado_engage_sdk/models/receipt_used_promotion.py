from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"promotion_id": "promotionId", "coupon_id": "couponId"})
class ReceiptUsedPromotion(BaseModel):
    """ReceiptUsedPromotion

    :param promotion_id: promotion_id, defaults to None
    :type promotion_id: str, optional
    :param coupon_id: coupon_id, defaults to None
    :type coupon_id: str, optional
    """

    def __init__(self, promotion_id: str = None, coupon_id: str = None):
        if promotion_id is not None:
            self.promotion_id = promotion_id
        if coupon_id is not None:
            self.coupon_id = coupon_id
