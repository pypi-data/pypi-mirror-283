from __future__ import annotations

__all__ = (
    "create_user_link",
    "create_bot_deeplink",
    "create_group_deeplink",
    "create_channel_deeplink",
    "create_game_deeplink",
    "create_webapp_deeplink",
    "is_valid_username",
    "is_valid_deeplink_parameter",
)

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from yatbaf.enums import AdminFlag
    from yatbaf.typing import NoneStr

DEEPLINK_PAYLOAD_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{,64}$")
USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_]{4,32}$")


def is_valid_username(username: str, /) -> bool:
    return bool(USERNAME_PATTERN.match(username))


def is_valid_deeplink_parameter(param: str, /) -> bool:
    return bool(DEEPLINK_PAYLOAD_PATTERN.match(param))


def create_user_link(username: str) -> str:
    """Returns link used to share public users, groups and channels

    See: https://core.telegram.org/api/links#public-username-links

    :param username: Public username.
    :raises ValueError: if username contains invalid chars.
    """

    if not is_valid_username(username):
        raise ValueError("Username is invalid.")
    return f"https://t.me/{username}"


def _check_deeplink_parameter(parameter: str) -> None:
    if not is_valid_deeplink_parameter(parameter):
        raise ValueError(
            "`parameter` can contain only following characters: "
            "a-z, A-Z, 0-9, '_', '-'"
        )


def create_bot_deeplink(bot_username: str, parameter: NoneStr = None) -> str:
    """Returns deep link used to link to bots.

    See: https://core.telegram.org/api/links#bot-links

    :param bot_username: Bot username.
    :param parameter: Start parameter, up to 64 base64url characters: if
        provided and the bot_username is indeed a bot, the text input bar should
        be replaced with a Start button (even if the user has already started
        the bot) that should invoke messages.startBot with the appropriate
        parameter once clicked.
    :raises ValueError: if ``bot_username`` or ``parameter`` contains invalid
        chars.
    """

    link = create_user_link(bot_username)
    if parameter:
        _check_deeplink_parameter(parameter)
        link += f"?start={parameter}"

    return link


def create_group_deeplink(
    bot_username: str,
    parameter: NoneStr = None,
    admin: list[AdminFlag] | None = None,
) -> str:
    """Returns deep link used to add bots to groups.

    See: https://core.telegram.org/api/links#groupchannel-bot-links

    :param bot_username: Bot username
    :param parameter: *Optional.* Start parameter, up to 64 base64url
        characters: if provided and the bot_username is indeed a bot,
        messages.startBot with the appropriate parameter should be invoked after
        adding the bot to the group.
    :param admin: *Optional.* A list of identifiers.
    :raises ValueError: if ``bot_username`` or ``parameter`` contains invalid
        chars.
    """

    link = create_user_link(bot_username) + "?startgroup"
    if parameter:
        _check_deeplink_parameter(parameter)
        link += f"={parameter}"

    if admin:
        link += f"&admin={'+'.join(admin)}"

    return link


def create_channel_deeplink(
    bot_username: str,
    admin: list[AdminFlag],
) -> str:
    """Returns deep link used to add bots to channels.

    See: https://core.telegram.org/api/links#groupchannel-bot-links

    :param bot_username: Bot username
    :param admin: A list of identifiers.
    :raises ValueError: if ``bot_username`` contains invalid chars or ``admin``
        is empty.
    """

    if not admin:
        raise ValueError("`admin` can't be empty.")

    return (
        create_user_link(bot_username) +
        f"?startchannel&admin={'+'.join(admin)}"
    )


def create_game_deeplink(bot_username: str, short_name: str) -> str:
    """Returns deep link used to share games.

    See: https://core.telegram.org/api/links#game-links

    :param bot_username: Username of the bot that owns the game.
    :param short_name: Game short name.
    :raises ValueError: if ``bot_username`` contains invalid chars.
    """

    return create_user_link(bot_username) + f"?game={short_name}"


def create_webapp_deeplink(
    bot_username: str,
    short_name: str,
    parameter: NoneStr = None,
) -> str:
    """Returns deep link used to share named bot web apps.

    See: https://core.telegram.org/api/links#named-bot-web-app-links

    :param bot_username: Username of the bot that owns the web app.
    :param short_name: Web app short name.
    :param parameter: *Optional.* `start_param` to pass to
        messages.requestAppWebView.
    :raises ValueError: if ``bot_username`` or ``parameter`` contains invalid
        chars.
    """

    link = create_user_link(bot_username) + f"/{short_name}?startapp"
    if parameter:
        _check_deeplink_parameter(parameter)
        link += f"={parameter}"

    return link
