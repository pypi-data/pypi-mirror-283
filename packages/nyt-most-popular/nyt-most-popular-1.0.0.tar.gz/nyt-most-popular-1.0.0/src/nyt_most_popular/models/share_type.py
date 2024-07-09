from enum import Enum


class ShareType(Enum):
    """An enumeration representing different categories.

    :cvar FACEBOOK: "facebook"
    :vartype FACEBOOK: str
    """

    FACEBOOK = "facebook"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, ShareType._member_map_.values()))
