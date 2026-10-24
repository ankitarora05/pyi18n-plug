"""Console entry point: ``pyi18n-plug``."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .core import I18n, is_rtl
from .loader import save_json

_PLURAL_KEYS = {"zero", "one", "two", "few", "many", "other"}


def cmd_demo(_args: argparse.Namespace) -> int:
    i18n = I18n()
    bar = "=" * 56
    print(bar)
    print("pyi18n-plug  demo  —  built-in locales")
    print(bar)
    print("Available:", ", ".join(i18n.available_locales()))
    print()
    for loc in i18n.available_locales():
        i18n.set_locale(loc)
        tag = " (RTL)" if is_rtl(loc) else ""
        print(f"[{loc}]{tag}")
        print(f"  t(greeting, name=World) -> {i18n.t('greeting', name='World')}")
        print(f"  t(welcome)              -> {i18n.t('welcome')}")
        print(f"  plural(items, 1)        -> {i18n.plural('items', 1)}")
        print(f"  plural(items, 5)        -> {i18n.plural('items', 5)}")
        print()
    print(bar)
    print("OK — install any JSON into ./locales/ and call i18n.load_directory().")
    return 0


def cmd_list(_args: argparse.Namespace) -> int:
    i18n = I18n()
    for loc in i18n.available_locales():
        print(loc + (" [rtl]" if is_rtl(loc) else ""))
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    path = Path(f"{args.locale}.json")
    if path.exists() and not args.force:
        print(f"{path} exists. Use --force to overwrite.", file=sys.stderr)
        return 1
    save_json(
        path,
        {
            "greeting": "Hello, {name}!",
            "welcome": "Welcome.",
            "items": {"one": "{count} item", "other": "{count} items"},
        },
    )
    print(f"Created {path}")
    return 0


def cmd_translate(args: argparse.Namespace) -> int:
    i18n = I18n()
    if args.locale:
        i18n.set_locale(args.locale)
    params: dict = {}
    for spec in args.param or []:
        k, _, v = spec.partition("=")
        if not k:
            continue
        params[k] = int(v) if k == "count" and v.lstrip("-").isdigit() else v
    print(i18n.t(args.key, **params))
    return 0


def _walk_keys(node: dict, prefix: str = ""):
    for k, v in node.items():
        p = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict) and not all(x in _PLURAL_KEYS for x in v):
            yield from _walk_keys(v, p)
        else:
            yield p


def cmd_validate(args: argparse.Namespace) -> int:
    i18n = I18n()
    try:
        i18n.load_directory(args.directory)
    except Exception as exc:  # pragma: no cover - defensive
        print(f"error: {exc}", file=sys.stderr)
        return 1

    baseline = set(_walk_keys(i18n._catalogs.get("en", {})))  # noqa: SLF001
    issues = 0
    for loc, cat in i18n._catalogs.items():  # noqa: SLF001
        if loc == "en":
            continue
        for missing in sorted(baseline - set(_walk_keys(cat))):
            print(f"✗ {loc}: missing key {missing!r}")
            issues += 1

    if issues:
        print(f"\n{issues} issue(s) found.")
        return 1
    print(f"✓ {len(i18n._catalogs)} catalog(s) valid")  # noqa: SLF001
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="pyi18n-plug",
        description="pyi18n-plug command line interface.",
    )
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("demo", help="Print sample translations for every built-in locale")
    sub.add_parser("list", help="List registered locales")

    p_init = sub.add_parser("init", help="Create a starter JSON catalog")
    p_init.add_argument("locale")
    p_init.add_argument("--force", action="store_true")

    p_tr = sub.add_parser("translate", help="Translate a key from the CLI")
    p_tr.add_argument("key")
    p_tr.add_argument("-l", "--locale")
    p_tr.add_argument("-p", "--param", action="append", metavar="key=value")

    p_val = sub.add_parser("validate", help="Validate every catalog in a directory")
    p_val.add_argument("directory", nargs="?", default=".")

    args = parser.parse_args(argv)
    if not args.cmd:
        parser.print_help()
        return 0
    return globals()[f"cmd_{args.cmd}"](args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())