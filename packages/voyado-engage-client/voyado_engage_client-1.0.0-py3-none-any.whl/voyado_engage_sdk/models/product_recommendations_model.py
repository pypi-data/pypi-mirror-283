from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class ProductRecommendationsModel(BaseModel):
    """ProductRecommendationsModel

    :param skus: skus, defaults to None
    :type skus: List[str], optional
    """

    def __init__(self, skus: List[str] = None):
        if skus is not None:
            self.skus = skus
