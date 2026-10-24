"""Runnable example — ``python examples/demo.py``."""
from pyi18n import I18n, is_rtl


def main() -> None:
    i18n = I18n(default_locale="en")     # English is active on install

    # Register a brand-new language at runtime (no files needed)
    i18n.register_locale(
        "es",
        data={
            "greeting": "Hola, {name}!",
            "welcome": "Bienvenido a pyi18n-plug.",
            "items": {"one": "{count} elemento", "other": "{count} elementos"},
        },
    )

    for loc in i18n.available_locales():
        i18n.set_locale(loc)
        tag = " [RTL]" if is_rtl(loc) else ""
        print(f"[{loc}]{tag}  {i18n.t('greeting', name='World')}")
        print(f"        {i18n.plural('items', 2)}")
    print(f"\nActive locale: {i18n.locale}  direction: {i18n.direction}")


if __name__ == "__main__":
    main()