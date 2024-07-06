from enum import Enum


class ChallengeGetChallengesFilter(Enum):
    """An enumeration representing different categories.

    :cvar ALL: "All"
    :vartype ALL: str
    :cvar ACTIVE: "Active"
    :vartype ACTIVE: str
    :cvar COMPLETED: "Completed"
    :vartype COMPLETED: str
    :cvar NOTCOMPLETED: "NotCompleted"
    :vartype NOTCOMPLETED: str
    """

    ALL = "All"
    ACTIVE = "Active"
    COMPLETED = "Completed"
    NOTCOMPLETED = "NotCompleted"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, ChallengeGetChallengesFilter._member_map_.values())
        )
