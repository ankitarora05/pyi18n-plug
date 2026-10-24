"""Catalog loading from disk or in-memory dicts."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .exceptions import CatalogError


def load_json(path: Path | str) -> dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise CatalogError(f"Catalog not found: {p}")
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CatalogError(f"Invalid JSON in {p}: {exc}") from exc
    if not isinstance(data, dict):
        raise CatalogError(f"Catalog {p} must be a JSON object")
    return data


def load_from_dict(data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise CatalogError("Catalog data must be a dict")
    return dict(data)


def save_json(path: Path | str, data: dict[str, Any]) -> None:
    Path(path).write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )