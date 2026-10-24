import pytest

from pyi18n import I18n


@pytest.mark.parametrize(
    "locale,count,expected",
    [
        ("en", 1, "1 item"),
        ("en", 5, "5 items"),
        ("de", 1, "1 Element"),
        ("de", 5, "5 Elemente"),
        ("fr", 1, "1 élément"),
        ("fr", 5, "5 éléments"),
        ("it", 1, "1 elemento"),
        ("it", 5, "5 elementi"),
        ("zh", 1, "1 个项目"),
        ("zh", 5, "5 个项目"),
    ],
)
def test_plural(locale, count, expected):
    i = I18n(); i.set_locale(locale)
    assert i.plural("items", count) == expected


def test_t_handles_plural_with_count():
    assert I18n().t("items", count=3) == "3 items"


def test_plural_with_babel_french_zero():
    pytest.importorskip("babel")
    i = I18n(); i.set_locale("fr")
    # French CLDR: 0 and 1 use "one"
    assert i.plural("items", 0) == "0 élément"


def test_plural_non_dict_returns_string():
    assert I18n().plural("greeting", 1, name="X") == "Hello, X!"


def test_plural_missing_key_returns_key():
    assert I18n().plural("nope", 1) == "nope"