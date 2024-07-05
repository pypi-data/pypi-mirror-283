from __future__ import annotations

__all__ = (
    "escape",
    "escape_f",
    "escape_code",
    "escape_link",
    "bold",
    "italic",
    "underline",
    "strikethrough",
    "spoiler",
    "url",
    "mention",
    "emoji",
    "inline",
    "code",
)

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Final

REPL: Final = r"\\\1"
PATTERN_TEXT: Final = re.compile(f'([{re.escape(r"_*[]()~`>#+-=|{}.!")}])')
PATTERN_FSTRING: Final = re.compile(f'([{re.escape(r"_*[]()~`>#+-=|.!")}])')
PATTERN_CODE_PRE: Final = re.compile(r"([\\\`])")
PATTERN_LINK_EMOJI: Final = re.compile(r"([\\\\\)])")


def escape(text: str, /) -> str:
    """Use this to escape markdown characters in text."""
    return PATTERN_TEXT.sub(REPL, text)


def escape_f(text: str, /) -> str:
    """Use this to escape markdown characters in f-string template."""
    return PATTERN_FSTRING.sub(REPL, text)


def escape_link(text: str, /) -> str:
    """Use this to escape markdown characters in link or emoji."""
    return PATTERN_LINK_EMOJI.sub(REPL, text)


def escape_code(text: str, /) -> str:
    """Use this to escape markdown characters in code."""
    return PATTERN_CODE_PRE.sub(REPL, text)


def bold(text: str, /) -> str:
    return f"*{text}*"


def italic(text: str, /) -> str:
    return f"_{text}_"


def underline(text: str, /) -> str:
    return f"__{text}__"


def strikethrough(text: str, /) -> str:
    return f"~{text}~"


def spoiler(text: str, /) -> str:
    return f"||{text}||"


def url(text: str, url: str, /) -> str:
    return f"[{text}]({url})"


def mention(username: str, user_id: int, /) -> str:
    return f"[{username}](tg://user?id={user_id})"


def emoji(emoji_id: int, placeholder_emoji: str, /) -> str:
    return f"![{placeholder_emoji}](tg://emoji?id={emoji_id})"


def inline(text: str, /) -> str:
    return f"`{text}`"


def code(text: str, /, lang: str = "") -> str:
    return f"```{lang}\n{text}\n```"
