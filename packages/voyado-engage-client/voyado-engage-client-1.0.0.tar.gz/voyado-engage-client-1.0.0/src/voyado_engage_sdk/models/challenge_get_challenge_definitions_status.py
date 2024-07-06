from enum import Enum


class ChallengeGetChallengeDefinitionsStatus(Enum):
    """An enumeration representing different categories.

    :cvar ALL: "All"
    :vartype ALL: str
    :cvar ACTIVE: "Active"
    :vartype ACTIVE: str
    :cvar DRAFT: "Draft"
    :vartype DRAFT: str
    :cvar SCHEDULED: "Scheduled"
    :vartype SCHEDULED: str
    :cvar ENDED: "Ended"
    :vartype ENDED: str
    """

    ALL = "All"
    ACTIVE = "Active"
    DRAFT = "Draft"
    SCHEDULED = "Scheduled"
    ENDED = "Ended"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(
                lambda x: x.value,
                ChallengeGetChallengeDefinitionsStatus._member_map_.values(),
            )
        )
