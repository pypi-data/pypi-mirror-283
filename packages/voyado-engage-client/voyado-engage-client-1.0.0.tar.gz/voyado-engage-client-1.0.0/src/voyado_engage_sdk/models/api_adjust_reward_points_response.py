from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({"contact_id": "contactId", "total_reward_points": "totalRewardPoints"})
class ApiAdjustRewardPointsResponse(BaseModel):
    """ApiAdjustRewardPointsResponse

    :param contact_id: contact_id
    :type contact_id: str
    :param total_reward_points: total_reward_points
    :type total_reward_points: float
    """

    def __init__(self, contact_id: str, total_reward_points: float):
        self.contact_id = contact_id
        self.total_reward_points = total_reward_points
