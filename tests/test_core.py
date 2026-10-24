import json

import pytest

from pyi18n import I18n, is_rtl
from pyi18n.exceptions import LocaleNotFoundError


def test_default_is_english():
    assert I18n().locale == "en"


def test_all_builtins_loaded():
    assert set(I18n().available_locales()) >= {
        "en", "de", "fr", "it", "hi", "ur", "zh"
    }


def test_translate_english():
    assert I18n().t("greeting", name="World") == "Hello, World!"


def test_translate_german():
    i = I18n(); i.set_locale("de")
    assert i.t("greeting", name="Welt") == "Hallo, Welt!"


def test_translate_french():
    i = I18n(); i.set_locale("fr")
    assert i.t("greeting", name="Monde") == "Bonjour, Monde !"


def test_translate_italian():
    i = I18n(); i.set_locale("it")
    assert i.t("greeting", name="Mondo") == "Ciao, Mondo!"


def test_translate_hindi():
    i = I18n(); i.set_locale("hi")
    assert i.t("greeting", name="दुनिया").startswith("नमस्ते")


def test_translate_urdu_and_rtl():
    i = I18n(); i.set_locale("ur")
    assert is_rtl(i.locale) is True
    assert i.direction == "rtl"
    assert "ہیلو" in i.t("greeting", name="دنیا")


def test_translate_chinese():
    i = I18n(); i.set_locale("zh")
    assert i.t("greeting", name="世界") == "你好，世界！"


def test_missing_key_returns_key():
    assert I18n().t("does.not.exist") == "does.not.exist"


def test_missing_placeholder_preserved():
    assert I18n().t("greeting") == "Hello, {name}!"


def test_callable_alias():
    assert I18n()("greeting", name="X") == "Hello, X!"


def test_has():
    i = I18n()
    assert i.has("greeting")
    assert not i.has("nope")


def test_set_unknown_locale_raises():
    with pytest.raises(LocaleNotFoundError):
        I18n().set_locale("xx")


def test_register_and_switch():
    i = I18n()
    i.register_locale("es", {"greeting": "Hola, {name}!"})
    i.set_locale("es")
    assert i.t("greeting", name="Mundo") == "Hola, Mundo!"


def test_register_from_file(tmp_path):
    p = tmp_path / "pt.json"
    p.write_text(json.dumps({"greeting": "Olá, {name}!"}), encoding="utf-8")
    i = I18n()
    i.register_locale("pt", path=p)
    i.set_locale("pt")
    assert i.t("greeting", name="Mundo") == "Olá, Mundo!"


def test_load_directory(tmp_path):
    (tmp_path / "es.json").write_text(
        json.dumps({"greeting": "Hola, {name}!"}), encoding="utf-8"
    )
    (tmp_path / "pt.json").write_text(
        json.dumps({"greeting": "Olá, {name}!"}), encoding="utf-8"
    )
    i = I18n()
    assert i.load_directory(tmp_path) == 2
    i.set_locale("es")
    assert i.t("greeting", name="X") == "Hola, X!"


def test_fallback_to_english():
    i = I18n()
    i.register_locale("xx", {"greeting": "X {name}!"})
    i.set_locale("xx")
    assert i.t("greeting", name="A") == "X A!"
    assert i.t("welcome") == "Welcome to pyi18n-plug."  # from en


def test_override_protection():
    i = I18n()
    i.register_locale("es", {"greeting": "uno"})
    i.register_locale("es", {"greeting": "dos"}, override=False)
    i.set_locale("es")
    assert i.t("greeting") == "uno"


def test_unregister_locale_resets_current():
    i = I18n(); i.set_locale("de")
    i.unregister_locale("de")
    assert i.locale == "en"


def test_is_rtl():
    assert is_rtl("ur")
    assert is_rtl("ur-PK")
    assert not is_rtl("en")
    assert not is_rtl("hi")