"""Module for all enum class"""

from enum import Enum, unique


@unique
class Canal(Enum):
    """
    Channel enum

    Args:
        Enum (Enum): Enum
    """

    GENERAL = "cMK"
    COMMERCE = "cMK:"
    RECRUTEMENT = "cMK?"
    GUILDE = "cMK%"


@unique
class PercoId(Enum):
    """
    Perco id enum

    Args:
        Enum (Enum): Enum
    """

    ADD_SELF = "gITM"
    ADD_OTHER = "gTS"
    REMOVE = "gTG"
    ATTACK = "gAA"
    SURVIVED = "gAS"
    LOOSE = "gAD"


@unique
class LogoChanel(Enum):
    """
    Logo channel enum

    Args:
        Enum (Enum): Enum
    """

    GENERAL = "⚪"
    COMMERCE = "🟤"
    RECRUTEMENT = "🟡"
    GUILDE = "🟣"
    BOT_ON = "🟢"
    BOT_OFF = "🔴"
    PERCO = ":unicorn:"
    PERCO_ATTACK = ":warning:"
    NB_PERCO = ":rage:"


@unique
class RolesHexa(Enum):
    """
    Roles hexa enum

    Args:
        Enum (Enum): Enum
    """

    EVERYONE = "@everyone"
