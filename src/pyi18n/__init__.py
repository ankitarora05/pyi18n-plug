"""pyi18n-plug — lightweight, plugin-style internationalization."""
from .core import DEFAULT_LOCALE, RTL_LOCALES, I18n, is_rtl
from .exceptions import CatalogError, I18nError, LocaleNotFoundError

__version__ = "0.1.0"
__all__ = [
    "I18n",
    "is_rtl",
    "RTL_LOCALES",
    "DEFAULT_LOCALE",
    "I18nError",
    "LocaleNotFoundError",
    "CatalogError",
    "__version__",
]