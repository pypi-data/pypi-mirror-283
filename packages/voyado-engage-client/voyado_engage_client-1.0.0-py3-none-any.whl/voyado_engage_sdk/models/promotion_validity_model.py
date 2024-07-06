from __future__ import annotations
from .utils.json_map import JsonMap
from .base import BaseModel
from .assign_date_range import AssignDateRange


@JsonMap(
    {
        "start_date": "startDate",
        "end_date": "endDate",
        "assigned_validity": "assignedValidity",
    }
)
class PromotionValidityModel(BaseModel):
    """Following class holds the duration information for a promotion.
    The this object uses to set and get the duration of a promotion.

    :param start_date: Start date when the promotion going to be active
    :type start_date: str
    :param end_date: End date when the promotion not longer active, defaults to None
    :type end_date: str, optional
    :param assigned_validity: The validity time of the promotion set when assignment occured, defaults to None
    :type assigned_validity: AssignDateRange, optional
    """

    def __init__(
        self,
        start_date: str,
        end_date: str = None,
        assigned_validity: AssignDateRange = None,
    ):
        self.start_date = start_date
        if end_date is not None:
            self.end_date = end_date
        if assigned_validity is not None:
            self.assigned_validity = self._define_object(
                assigned_validity, AssignDateRange
            )
