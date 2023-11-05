from enum import Enum, unique


@unique
class Canal(Enum):
    GENERAL = "cMK"
    COMMERCE = "cMK:"
    RECRUTEMENT = "cMK?"
    GUILDE = "cMK%"


@unique
class PercoId(Enum):
    ADD_SELF = "gITM"
    ADD_OTHER = "gTS"
    REMOVE = "gTG"
    ATTACK = "gAA"
    SURVIVED = "gAS"
    LOOSE = "gAD"


@unique
class LogoChanel(Enum):
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
    EVERYONE = "@everyone"
