import json

import pytest

from pyi18n.exceptions import CatalogError
from pyi18n.loader import load_from_dict, load_json, save_json


def test_load_json(tmp_path):
    p = tmp_path / "en.json"
    p.write_text(json.dumps({"a": 1}), encoding="utf-8")
    assert load_json(p) == {"a": 1}


def test_load_missing(tmp_path):
    with pytest.raises(CatalogError):
        load_json(tmp_path / "nope.json")


def test_load_bad_json(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("{not json", encoding="utf-8")
    with pytest.raises(CatalogError):
        load_json(p)


def test_load_non_object(tmp_path):
    p = tmp_path / "list.json"
    p.write_text(json.dumps([1, 2]), encoding="utf-8")
    with pytest.raises(CatalogError):
        load_json(p)


def test_load_from_dict():
    assert load_from_dict({"a": 1}) == {"a": 1}


def test_load_from_dict_invalid():
    with pytest.raises(CatalogError):
        load_from_dict([1])  # type: ignore[arg-type]


def test_save_roundtrip(tmp_path):
    p = tmp_path / "x.json"
    save_json(p, {"greeting": "X"})
    assert load_json(p) == {"greeting": "X"}