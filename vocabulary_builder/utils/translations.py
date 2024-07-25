import gettext
from enum import Enum
from pathlib import Path


class LanguageModel(str, Enum):
    """Enumeration of supported languages."""

    ru = "ru"
    uk = "uk"
    fr = "fr"
    de = "de"


def _(language: str):
    """
    Retrieve the gettext translation function for the specified language.

    :param language: Language code (e.g., 'ru', 'fr').
    :return: The translation function for the specified language.
    """
    try:
        translations = gettext.translation(
            domain="translations",
            localedir=Path(__file__).parent.parent.absolute() / "locales",
            languages=[language],
        )
    except FileNotFoundError:
        translations = gettext.NullTranslations()
    return translations.gettext
