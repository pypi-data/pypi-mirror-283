from enum import Enum


class GetViewedPeriodJsonPeriod(Enum):
    """An enumeration representing different categories.

    :cvar _1: 1
    :vartype _1: str
    :cvar _7: 7
    :vartype _7: str
    :cvar _30: 30
    :vartype _30: str
    """

    _1 = 1
    _7 = 7
    _30 = 30

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, GetViewedPeriodJsonPeriod._member_map_.values())
        )
