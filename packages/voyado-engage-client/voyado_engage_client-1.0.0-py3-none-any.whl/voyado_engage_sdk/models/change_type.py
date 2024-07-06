from enum import Enum


class ChangeType(Enum):
    """An enumeration representing different categories.

    :cvar CREATED: "Created"
    :vartype CREATED: str
    :cvar UPDATED: "Updated"
    :vartype UPDATED: str
    :cvar DELETED: "Deleted"
    :vartype DELETED: str
    """

    CREATED = "Created"
    UPDATED = "Updated"
    DELETED = "Deleted"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, ChangeType._member_map_.values()))
