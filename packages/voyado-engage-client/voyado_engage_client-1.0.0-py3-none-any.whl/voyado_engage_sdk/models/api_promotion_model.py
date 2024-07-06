from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .api_promotion_redemption_channel_model import ApiPromotionRedemptionChannelModel


@JsonMap(
    {
        "id_": "id",
        "promotion_id": "promotionId",
        "external_id": "externalId",
        "type_": "type",
        "expires_on": "expiresOn",
        "redeemed_on": "redeemedOn",
        "image_url": "imageUrl",
        "redemption_channels": "redemptionChannels",
    }
)
class ApiPromotionModel(BaseModel):
    """ApiPromotionModel

    :param id_: id_, defaults to None
    :type id_: str, optional
    :param promotion_id: promotion_id, defaults to None
    :type promotion_id: str, optional
    :param external_id: external_id, defaults to None
    :type external_id: str, optional
    :param type_: type_, defaults to None
    :type type_: str, optional
    :param name: name, defaults to None
    :type name: str, optional
    :param expires_on: expires_on, defaults to None
    :type expires_on: str, optional
    :param heading: heading, defaults to None
    :type heading: str, optional
    :param description: description, defaults to None
    :type description: str, optional
    :param redeemed: redeemed, defaults to None
    :type redeemed: bool, optional
    :param redeemed_on: redeemed_on, defaults to None
    :type redeemed_on: str, optional
    :param image_url: image_url, defaults to None
    :type image_url: str, optional
    :param link: link, defaults to None
    :type link: str, optional
    :param redemption_channels: redemption_channels, defaults to None
    :type redemption_channels: List[ApiPromotionRedemptionChannelModel], optional
    """

    def __init__(
        self,
        id_: str = None,
        promotion_id: str = None,
        external_id: str = None,
        type_: str = None,
        name: str = None,
        expires_on: str = None,
        heading: str = None,
        description: str = None,
        redeemed: bool = None,
        redeemed_on: str = None,
        image_url: str = None,
        link: str = None,
        redemption_channels: List[ApiPromotionRedemptionChannelModel] = None,
    ):
        if id_ is not None:
            self.id_ = id_
        if promotion_id is not None:
            self.promotion_id = promotion_id
        if external_id is not None:
            self.external_id = external_id
        if type_ is not None:
            self.type_ = type_
        if name is not None:
            self.name = name
        if expires_on is not None:
            self.expires_on = expires_on
        if heading is not None:
            self.heading = heading
        if description is not None:
            self.description = description
        if redeemed is not None:
            self.redeemed = redeemed
        if redeemed_on is not None:
            self.redeemed_on = redeemed_on
        if image_url is not None:
            self.image_url = image_url
        if link is not None:
            self.link = link
        if redemption_channels is not None:
            self.redemption_channels = self._define_list(
                redemption_channels, ApiPromotionRedemptionChannelModel
            )
