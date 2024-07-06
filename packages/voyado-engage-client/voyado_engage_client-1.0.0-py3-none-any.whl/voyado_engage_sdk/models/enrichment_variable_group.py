from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .enrichment_variable import EnrichmentVariable


@JsonMap({"bci_group_id": "bciGroupId", "group_name": "groupName"})
class EnrichmentVariableGroup(BaseModel):
    """Grouped BCI enrichment varioables

    :param bci_group_id: BCI group identifier, defaults to None
    :type bci_group_id: str, optional
    :param group_name: Group name in Voyado, defaults to None
    :type group_name: str, optional
    :param variables: Variables in group, defaults to None
    :type variables: List[EnrichmentVariable], optional
    """

    def __init__(
        self,
        bci_group_id: str = None,
        group_name: str = None,
        variables: List[EnrichmentVariable] = None,
    ):
        if bci_group_id is not None:
            self.bci_group_id = bci_group_id
        if group_name is not None:
            self.group_name = group_name
        if variables is not None:
            self.variables = self._define_list(variables, EnrichmentVariable)
