from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .promotion_validity_model import PromotionValidityModel
from .promotion_basic_presentation_model import PromotionBasicPresentationModel
from .multichannel_promotion_redemption_channel_model import (
    MultichannelPromotionRedemptionChannelModel,
)


@JsonMap({"external_id": "externalId", "redemption_channels": "redemptionChannels"})
class MultichannelBasePromotionModel(BaseModel):
    """MultichannelBasePromotionModel

    :param external_id: External id generated from system outside of Voyado, defaults to None
    :type external_id: str, optional
    :param name: Name of promtion.
    <br>Following field is required and don't allows to be left out or set to null or empty string
    :type name: str
    :param validity: Following class holds the duration information for a promotion.
    <br>The this object uses to set and get the duration of a promotion., defaults to None
    :type validity: PromotionValidityModel, optional
    :param presentation: Following object is for get/set the presentational side of the promotion.
    <br>This data uses to displey in different kind of views, for an example in Email messages etc.
    <br>
    <br>This fields populates the "Presentation" section in the admin UI., defaults to None
    :type presentation: PromotionBasicPresentationModel, optional
    :param redemption_channels: Redemption channels
    <br>Valid channels: POS, ECOM and OTHER, defaults to None
    :type redemption_channels: List[MultichannelPromotionRedemptionChannelModel], optional
    """

    def __init__(
        self,
        name: str,
        external_id: str = None,
        validity: PromotionValidityModel = None,
        presentation: PromotionBasicPresentationModel = None,
        redemption_channels: List[MultichannelPromotionRedemptionChannelModel] = None,
    ):
        if external_id is not None:
            self.external_id = external_id
        self.name = name
        if validity is not None:
            self.validity = self._define_object(validity, PromotionValidityModel)
        if presentation is not None:
            self.presentation = self._define_object(
                presentation, PromotionBasicPresentationModel
            )
        if redemption_channels is not None:
            self.redemption_channels = self._define_list(
                redemption_channels, MultichannelPromotionRedemptionChannelModel
            )
