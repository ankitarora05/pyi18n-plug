class I18nError(Exception):
    """Base class for all pyi18n-plug errors."""


class LocaleNotFoundError(I18nError):
    """Raised when a locale is requested but not registered."""


class CatalogError(I18nError):
    """Raised when a catalog file is missing or malformed."""