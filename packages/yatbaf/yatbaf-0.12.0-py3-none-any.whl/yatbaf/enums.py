__all__ = (
    "ParseMode",
    "Event",
    "ChatAction",
    "StickerType",
    "StickerFormat",
    "ThumbnailMimeType",
    "VideoMimeType",
    "DocumentMimeType",
    "PassportElement",
    "PollType",
    "MessageEntityType",
    "ContentType",
    "ChatType",
    "IconColor",
    "Currency",
    "MaskPositionPoint",
    "BotEnvi",
    "MarkdownEntity",
    "AdminFlag",
)

from enum import Enum
from enum import IntEnum
from enum import StrEnum
from enum import auto


class ParseMode(StrEnum):
    """Message parse mode.

    See: https://core.telegram.org/bots/api#formatting-options
    """

    HTML = "HTML"
    MARKDOWN = "MarkdownV2"
    MARKDOWN_LEGACY = "Markdown"


class Event(StrEnum):
    """Available events.

    See :class:`~yatbaf.types.update.Update`
    """

    MESSAGE = auto()
    EDITED_MESSAGE = auto()
    CHANNEL_POST = auto()
    EDITED_CHANNEL_POST = auto()
    BUSINESS_CONNECTION = auto()
    BUSINESS_MESSAGE = auto()
    EDITED_BUSINESS_MESSAGE = auto()
    DELETED_BUSINESS_MESSAGES = auto()
    MESSAGE_REACTION = auto()
    MESSAGE_REACTION_COUNT = auto()
    INLINE_QUERY = auto()
    CHOSEN_INLINE_RESULT = auto()
    CALLBACK_QUERY = auto()
    SHIPPING_QUERY = auto()
    PRE_CHECKOUT_QUERY = auto()
    POLL = auto()
    POLL_ANSWER = auto()
    MY_CHAT_MEMBER = auto()
    CHAT_MEMBER = auto()
    CHAT_JOIN_REQUEST = auto()
    CHAT_BOOST = auto()
    REMOVED_CHAT_BOOST = auto()


class ChatAction(StrEnum):
    """Chat action.

    See :meth:`send_chat_action <yatbaf.bot.Bot.send_chat_action>`,
    https://core.telegram.org/bots/api#sendchataction
    """

    TYPING = auto()
    UPLOAD_PHOTO = auto()
    RECORD_VIDEO = auto()
    UPLOAD_VIDEO = auto()
    RECORD_VOICE = auto()
    UPLOAD_VOICE = auto()
    UPLOAD_DOCUMENT = auto()
    CHOOSE_STICKER = auto()
    FIND_LOCATION = auto()
    RECORD_VIDEO_NOTE = auto()
    UPLOAD_VIDEO_NOTE = auto()


class StickerType(StrEnum):
    REGULAR = auto()
    MASK = auto()
    CUSTOM_EMOJI = auto()


class StickerFormat(StrEnum):
    STATIC = auto()
    """For a .WEBP or .PNG image."""

    ANIMATED = auto()
    """For a .TGS animation."""

    VIDEO = auto()
    """For a WEBM video."""


class ThumbnailMimeType(StrEnum):
    JPEG = "image/jpeg"
    GIF = "image/gif"
    MP4 = "video/mp4"


class VideoMimeType(StrEnum):
    HTML = "text/html"
    MP4 = "video/mp4"


class DocumentMimeType(StrEnum):
    PDF = "application/pdf"
    ZIP = "application/zip"


class PassportElement(StrEnum):
    ADDRESS = auto()
    PASSPORT = auto()
    DRIVER_LICENSE = auto()
    IDENTITY_CARD = auto()
    INTERNAL_PASSPORT = auto()
    UTILITY_BILL = auto()
    BANK_STATEMENT = auto()
    RENTAL_AGREEMENT = auto()
    PASSPORT_REGISTRATION = auto()
    TEMPORARY_REGISTRATION = auto()
    PERSONAL_DETAILS = auto()
    PHONE_NUMBER = auto()
    EMAIL = auto()


class PollType(StrEnum):
    """Poll type."""

    QUIZ = auto()
    REGULAR = auto()


# https://core.telegram.org/bots/api#messageentity
class MessageEntityType(StrEnum):
    MENTION = auto()
    HASHTAG = auto()
    CASHTAG = auto()
    BOT_COMMAND = auto()
    URL = auto()
    EMAIL = auto()
    PHONE_NUMBER = auto()
    BOLD = auto()
    ITALIC = auto()
    UNDERLINE = auto()
    STRIKETHROUGH = auto()
    SPOILER = auto()
    CODE = auto()
    PRE = auto()
    TEXT_LINK = auto()
    TEXT_MENTION = auto()
    CUSTOM_EMOJI = auto()


class ContentType(StrEnum):
    """Message content type.

    See: :class:`Message <yatbaf.types.message.Message>`
    """

    TEXT = auto()
    ANIMATION = auto()
    AUDIO = auto()
    DOCUMENT = auto()
    PHOTO = auto()
    STICKER = auto()
    VIDEO = auto()
    VIDEO_NOTE = auto()
    VOICE = auto()
    CONTACT = auto()
    DICE = auto()
    GAME = auto()
    POLL = auto()
    VENUE = auto()
    LOCATION = auto()
    PASSPORT_DATA = auto()
    INVOICE = auto()
    WEB_APP_DATA = auto()
    SUCCESSFUL_PAYMENT = auto()

    NEW_CHAT_MEMBER = auto()
    LEFT_CHAT_MEMBER = auto()
    NEW_CHAT_PHOTO = auto()
    DELETE_CHAT_PHOTO = auto()
    GROUP_CHAT_CREATED = auto()
    SUPERGROUP_CHAT_CREATED = auto()
    CHANNEL_CHAT_CREATED = auto()
    MESSAGE_AUTO_DELETE_TIMER_CHANGED = auto()
    MIGRATE_TO_CHAT_ID = auto()
    MIGRATE_FROM_CHAT_ID = auto()
    PINNED_MESSAGE = auto()
    USERS_SHARED = auto()
    CHAT_SHARED = auto()
    CONNECTED_WEBSITE = auto()
    WRITE_ACCESS_ALLOWED = auto()
    PROXIMITY_ALERT_TRIGGERED = auto()
    FORUM_TOPIC_CREATED = auto()
    FORUM_TOPIC_EDITED = auto()
    FORUM_TOPIC_CLOSED = auto()
    FORUM_TOPIC_REOPENED = auto()
    GENERAL_FORUM_TOPIC_HIDDEN = auto()
    GENERAL_FORUM_TOPIC_UNHIDDEN = auto()
    VIDEO_CHAT_SCHEDULED = auto()
    VIDEO_CHAT_STARTED = auto()
    VIDEO_CHAT_ENDED = auto()
    VIDEO_CHAT_PARTICIPANTS_INVITED = auto()


class ChatType(StrEnum):
    """Chat type.

    See :attr:`Chat.type <yatbaf.types.chat.Chat.type>`
    """

    SENDER = auto()
    PRIVATE = auto()
    GROUP = auto()
    SUPERGROUP = auto()
    CHANNEL = auto()


class IconColor(IntEnum):
    BLUE = 7322096  # 6FB9F0
    YELLOW = 16766590  # FFD67E
    PURPLE = 13338331  # CB86DB
    GREEN = 9367192  # 8EEE98
    PINK = 16749490  # FF93B2
    RED = 16478047  # FB6F5F


class Currency(StrEnum):
    """Supported currencies

    See: https://core.telegram.org/bots/payments#supported-currencies
    """

    UNITED_ARAB_EMIRATES_DIRHAM = "AED"
    AFGHAN_AFGHANI = "AFN"
    ALBANIAN_LEK = "ALL"
    ARMENIAN_DRAM = "AMD"
    ARGENTINE_PESO = "ARS"
    AUSTRALIAN_DOLLAR = "AUD"
    AZERBAIJANI_MANAT = "AZN"
    BOSNIA_HERZEGOVINA_CONVERTIBLE_MARK = "BAM"
    BANGLADESHI_TAKA = "BDT"
    BULGARIAN_LEV = "BGN"
    BRUNEI_DOLLAR = "BND"
    BOLIVIAN_BOLIVIANO = "BOB"
    BRAZILIAN_REAL = "BRL"
    BELARUSIAN_RUBLE = "BYN"
    CANADIAN_DOLLAR = "CAD"
    SWISS_FRANC = "CHF"
    CHILEAN_PESO = "CLP"
    CHINESE_RENMINBI_YUAN = "CNY"
    COLOMBIAN_PESO = "COP"
    COSTA_RICAN_COLON = "CRC"
    CZECH_KORUNA = "CZK"
    DANISH_KRONE = "DKK"
    DOMINICAN_PESO = "DOP"
    ALGERIAN_DINAR = "DZD"
    EGYPTIAN_POUND = "EGP"
    ETHIOPIAN_BIRR = "ETB"
    EURO = "EUR"
    BRITISH_POUND = "GBP"
    GEORGIAN_LARI = "GEL"
    GUATEMALAN_QUETZAL = "GTQ"
    HONG_KONG_DOLLAR = "HKD"
    HONDURAN_LEMPIRA = "HNL"
    CROATIAN_KUNA = "HRK"
    HUNGARIAN_FORINT = "HUF"
    INDONESIAN_RUPIAH = "IDR"
    ISRAELI_NEW_SHEQEL = "ILS"
    INDIAN_RUPEE = "INR"
    ICELANDIC_KRONA = "ISK"
    JAMAICAN_DOLLAR = "JMD"
    JAPANESE_YEN = "JPY"
    KENYAN_SHILLING = "KES"
    KYRGYZSTANI_SOM = "KGS"
    SOUTH_KOREAN_WON = "KRW"
    KAZAKHSTANI_TENGE = "KZT"
    LEBANESE_POUND = "LBP"
    SRI_LANKAN_RUPEE = "LKR"
    MOROCCAN_DIRHAM = "MAD"
    MOLDOVAN_LEU = "MDL"
    MONGOLIAN_TOGROG = "MNT"
    MAURITIAN_RUPEE = "MUR"
    MALDIVIAN_RUFIYAA = "MVR"
    MEXICAN_PESO = "MXN"
    MALAYSIAN_RINGGIT = "MYR"
    MOZAMBICAN_METICAL = "MZN"
    NIGERIAN_NAIRA = "NGN"
    NICARAGUAN_CORDOBA = "NIO"
    NORWEGIAN_KRONE = "NOK"
    NEPALESE_RUPEE = "NPR"
    NEW_ZEALAND_DOLLAR = "NZD"
    PANAMANIAN_BALBOA = "PAB"
    PERUVIAN_NUEVO_SOL = "PEN"
    PHILIPPINE_PESO = "PHP"
    PAKISTANI_RUPEE = "PKR"
    POLISH_ZLOTY = "PLN"
    PARAGUAYAN_GUARANI = "PYG"
    QATARI_RIYAL = "QAR"
    ROMANIAN_LEU = "RON"
    SERBIAN_DINAR = "RSD"
    RUSSIAN_RUBLE = "RUB"
    SAUDI_RIYAL = "SAR"
    SWEDISH_KRONA = "SEK"
    SINGAPORE_DOLLAR = "SGD"
    THAI_BAHT = "THB"
    TAJIKISTANI_SOMONI = "TJS"
    TURKISH_LIRA = "TRY"
    TRINIDAD_AND_TOBAGO_DOLLAR = "TTD"
    NEW_TAIWAN_DOLLAR = "TWD"
    TANZANIAN_SHILLING = "TZS"
    UKRAINIAN_HRYVNIA = "UAH"
    UGANDAN_SHILLING = "UGX"
    UNITED_STATES_DOLLAR = "USD"
    URUGUAYAN_PESO = "UYU"
    UZBEKISTANI_SOM = "UZS"
    VIETNAMESE_DONG = "VND"
    YEMENI_RIAL = "YER"
    SOUTH_AFRICAN_RAND = "ZAR"
    TELEGRAM_STARS = "XTR"


class MaskPositionPoint(StrEnum):
    FOREHEAD = auto()
    EYES = auto()
    MOUTH = auto()
    CHIN = auto()


class BotEnvi(Enum):
    """See https://core.telegram.org/bots/features#dedicated-test-environment"""

    PROD = auto()
    TEST = auto()


class MarkdownEntity(StrEnum):
    """See https://core.telegram.org/bots/api#markdownv2-style"""

    TEXT = auto()
    """text"""
    FSTRING = auto()
    """text with f-string placeholder"""
    PRE = auto()
    """inline fixed-width code"""
    CODE = auto()
    """pre-formatted fixed-width code block"""
    LINK = auto()
    """inline url"""
    EMOJI = auto()
    """emoji"""


class AdminFlag(StrEnum):
    """See https://core.telegram.org/constructor/chatAdminRights#parameters"""

    CHANGE_INFO = auto()
    POST_MESSAGES = auto()
    EDIT_MESSAGES = auto()
    DELETE_MESSAGES = auto()
    RESTRICT_MEMBERS = auto()
    INVITE_USERS = auto()
    PIN_MESSAGES = auto()
    MANAGE_TOPICS = auto()
    PROMOTE_MEMBERS = auto()
    MANAGE_VIDEO_CHATS = auto()
    ANONYMOUS = auto()
    MANAGE_CHAT = auto()
