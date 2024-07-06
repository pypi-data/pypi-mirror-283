from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"redemption_channel": "redemptionChannel"})
class RedeemBodyModel(BaseModel):
    """RedeemBodyModel

    :param redemption_channel: redemption_channel, defaults to None
    :type redemption_channel: str, optional
    """

    def __init__(self, redemption_channel: str = None):
        if redemption_channel is not None:
            self.redemption_channel = redemption_channel
