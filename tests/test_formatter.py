from pyi18n.formatter import SafeFormatDict, safe_format


def test_basic_format():
    assert safe_format("Hi {name}", {"name": "Ann"}) == "Hi Ann"


def test_missing_placeholder_preserved():
    assert safe_format("Hi {name}", {}) == "Hi {name}"


def test_format_spec_ignored_safely():
    assert safe_format("N={count:,}", {}) == "N={count}"


def test_nested_missing():
    assert safe_format("{a}-{b}", {"a": "x"}) == "x-{b}"


def test_safe_format_dict():
    d = SafeFormatDict({"x": 1})
    assert str(d["missing"]) == "{missing}"