"""Safe placeholder substitution. Missing placeholders never raise."""
from __future__ import annotations


class _Missing:
    __slots__ = ("key",)

    def __init__(self, key: str) -> None:
        self.key = key

    def __format__(self, spec: str) -> str:  # ignore spec safely
        return "{" + self.key + "}"

    def __str__(self) -> str:
        return "{" + self.key + "}"


class SafeFormatDict(dict):
    def __missing__(self, key: str) -> _Missing:  # type: ignore[override]
        return _Missing(key)


def safe_format(template: str, params: dict) -> str:
    """Format ``template`` with ``params``; leave unknown placeholders intact."""
    try:
        return template.format_map(SafeFormatDict(params))
    except (KeyError, IndexError, ValueError):
        return template