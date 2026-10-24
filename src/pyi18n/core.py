"""Public API for pyi18n-plug."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .exceptions import CatalogError, LocaleNotFoundError
from .formatter import safe_format
from .loader import load_from_dict, load_json

DEFAULT_LOCALE = "en"
BUILTIN_DIR = Path(__file__).parent / "locales"

RTL_LOCALES: frozenset[str] = frozenset({"ar", "ur", "he", "fa", "yi"})

_PLURAL_CATEGORIES = frozenset(
    {"zero", "one", "two", "few", "many", "other"}
)

_NULL = object()


def is_rtl(locale: str) -> bool:
    """True if the locale's script is right-to-left."""
    return locale.split("-")[0].split("_")[0].lower() in RTL_LOCALES


def _walk(catalog: dict, dotted: str) -> Any:
    node: Any = catalog
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            return _NULL
        node = node[part]
    return node


def _select_plural_form(locale: str, count: int, forms: dict) -> str:
    """Pick the CLDR plural category for ``count`` in ``locale``."""
    try:  # try babel for full CLDR rules
        from babel.core import Locale as BabelLocale

        cat = BabelLocale.parse(locale, sep="-").plural_form(count)
        if cat in forms:
            return cat
    except Exception:  # babel missing or locale unknown
        pass

    # Fallback heuristics
    if count == 0 and "zero" in forms:
        return "zero"
    if count == 1 and "one" in forms:
        return "one"
    if count == 2 and "two" in forms:
        return "two"
    return "other"


class I18n:
    """A single i18n engine instance.

    Example::

        from pyi18n import I18n
        i18n = I18n()                                # defaults to English
        i18n.set_locale("hi")
        print(i18n.t("greeting", name="World"))
    """

    def __init__(
        self,
        default_locale: str = DEFAULT_LOCALE,
        fallback_locale: str | None = None,
        autoload_builtins: bool = True,
    ) -> None:
        self.default_locale = default_locale
        self.fallback_locale = fallback_locale or default_locale
        self._catalogs: dict[str, dict] = {}
        self._current: str = default_locale
        if autoload_builtins:
            self._load_builtins()

    # ------------------------------------------------------------------ #
    # Loading
    # ------------------------------------------------------------------ #
    def _load_builtins(self) -> None:
        for path in sorted(BUILTIN_DIR.glob("*.json")):
            try:
                self._catalogs[path.stem] = load_json(path)
            except CatalogError:
                continue  # never block on a corrupt shipped file

    def register_locale(
        self,
        code: str,
        data: dict | None = None,
        *,
        path: str | Path | None = None,
        override: bool = True,
    ) -> None:
        """Add or replace a locale catalog from an in-memory dict or JSON file."""
        if data is None and path is None:
            raise ValueError("Provide either 'data' or 'path'.")
        catalog = (
            load_from_dict(data) if data is not None else load_json(Path(path))  # type: ignore[arg-type]
        )
        if not override and code in self._catalogs:
            return
        self._catalogs[code] = catalog

    def load_directory(self, directory: str | Path, pattern: str = "*.json") -> int:
        """Load every ``*.json`` file in ``directory`` (filename stem = locale)."""
        d = Path(directory)
        if not d.is_dir():
            raise CatalogError(f"Not a directory: {d}")
        n = 0
        for path in sorted(d.glob(pattern)):
            self._catalogs[path.stem] = load_json(path)
            n += 1
        return n

    def unregister_locale(self, code: str) -> None:
        self._catalogs.pop(code, None)
        if self._current == code:
            self._current = self.default_locale

    # ------------------------------------------------------------------ #
    # Properties
    # ------------------------------------------------------------------ #
    @property
    def locale(self) -> str:
        return self._current

    @property
    def direction(self) -> str:
        return "rtl" if is_rtl(self._current) else "ltr"

    def available_locales(self) -> list[str]:
        return sorted(self._catalogs)

    # ------------------------------------------------------------------ #
    # Locale switching
    # ------------------------------------------------------------------ #
    def set_locale(self, code: str) -> None:
        if code not in self._catalogs:
            raise LocaleNotFoundError(f"Locale '{code}' is not registered.")
        self._current = code

    # ------------------------------------------------------------------ #
    # Translation
    # ------------------------------------------------------------------ #
    def _resolve(self, key: str) -> Any:
        chain = [self._current]
        if self.fallback_locale not in chain:
            chain.append(self.fallback_locale)
        if self.default_locale not in chain:
            chain.append(self.default_locale)
        for loc in chain:
            value = _walk(self._catalogs.get(loc, {}), key)
            if value is not _NULL:
                return value
        return _NULL

    def has(self, key: str) -> bool:
        return self._resolve(key) is not _NULL

    def t(self, key: str, /, **params: Any) -> str:
        """Translate ``key``. If it resolves to a plural dict, ``count`` selects the form."""
        value = self._resolve(key)
        if value is _NULL:
            return key
        if isinstance(value, dict):
            if "count" in params:
                return self.plural(
                    key,
                    int(params["count"]),
                    **{k: v for k, v in params.items() if k != "count"},
                )
            # dict without count: fall back to "other"
            value = value.get("other", key)
        if not isinstance(value, str):
            return key
        return safe_format(value, params)

    __call__ = t  # allow ``i18n("key", name="x")``

    def plural(self, key: str, count: int, /, **params: Any) -> str:
        """Select the CLDR plural form for ``count``."""
        value = self._resolve(key)
        if value is _NULL:
            return key
        if not isinstance(value, dict):
            return self.t(key, count=count, **params)

        category = _select_plural_form(self._current, count, value)
        template = value.get(category) or value.get("other")
        if not isinstance(template, str):
            return key
        return safe_format(template, {"count": count, **params})

    # ------------------------------------------------------------------ #
    # Optional formatting (requires babel; degrades gracefully)
    # ------------------------------------------------------------------ #
    def number(self, value: float, format: str | None = None) -> str:
        try:
            from babel.numbers import format_decimal

            return format_decimal(value, format=format, locale=self._current)
        except ImportError:
            return str(value)

    def currency(self, value: float, currency_code: str = "USD") -> str:
        try:
            from babel.numbers import format_currency

            return format_currency(value, currency_code, locale=self._current)
        except ImportError:
            return f"{value} {currency_code}"

    def datetime(self, value, format: str = "medium") -> str:
        try:
            from babel.dates import format_datetime

            return format_datetime(value, format=format, locale=self._current)
        except ImportError:
            return value.isoformat() if hasattr(value, "isoformat") else str(value)