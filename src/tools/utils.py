"""Module for all utils func"""


def update_escape_character(payload: str) -> str:
    """
    Update escape character

    Args:
        payload (str): payload

    Returns:
        str: payload
    """
    return (
        payload.replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
        .replace("&amp;", "&")
        .replace("&apos;", "'")
        .replace("&tilde;", "~")
        .replace("&circ;", "^")
        .replace("&grave;", "`")
        .replace("&eacute;", "é")
        .replace("&Eacute;", "É")
        .replace("&egrave;", "è")
        .replace("&Egrave;", "È")
        .replace("&ecirc;", "ê")
        .replace("°0", "[Item]")
    )
