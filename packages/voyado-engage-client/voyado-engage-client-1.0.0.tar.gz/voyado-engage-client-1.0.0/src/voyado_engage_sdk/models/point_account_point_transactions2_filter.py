from enum import Enum


class PointAccountPointTransactions2Filter(Enum):
    """An enumeration representing different categories.

    :cvar ALL: "All"
    :vartype ALL: str
    :cvar ACTIVE: "Active"
    :vartype ACTIVE: str
    :cvar PENDING: "Pending"
    :vartype PENDING: str
    """

    ALL = "All"
    ACTIVE = "Active"
    PENDING = "Pending"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(
                lambda x: x.value,
                PointAccountPointTransactions2Filter._member_map_.values(),
            )
        )
