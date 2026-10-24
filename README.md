# pyi18n-plug

> Lightweight, plugin-style internationalization for Python — JSON catalogs,
> CLDR plurals, RTL support, and a CLI. Zero hard dependencies.

[![PyPI version](https://img.shields.io/pypi/v/pyi18n-plug.svg)](https://pypi.org/project/pyi18n-plug/)
[![Python versions](https://img.shields.io/pypi/pyversions/pyi18n-plug.svg)](https://pypi.org/project/pyi18n-plug/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://github.com/your-org/pyi18n-plug/actions/workflows/tests.yml/badge.svg)](https://github.com/your-org/pyi18n-plug/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## Project tree

```
pyi18n-plug/
├── pyproject.toml
├── README.md
├── LICENSE
├── .gitignore
├── examples/
│   └── demo.py
├── src/
│   └── pyi18n/
│       ├── __init__.py
│       ├── py.typed
│       ├── core.py
│       ├── loader.py
│       ├── formatter.py
│       ├── exceptions.py
│       ├── cli.py
│       └── locales/
│           ├── en.json
│           ├── de.json
│           ├── fr.json
│           ├── it.json
│           ├── hi.json
│           ├── ur.json
│           └── zh.json
└── tests/
    ├── test_core.py
    ├── test_loader.py
    ├── test_formatter.py
    ├── test_plural.py
    └── test_cli.py
```

## Testing 

bash
python -c "
import sys; sys.path.insert(0, 'src')
from pyi18n import I18n
i = I18n()
for loc in i.available_locales():
    i.set_locale(loc)
    print(loc, '->', i.t('greeting', name='World'))
"

## Why pyi18n-plug

Most Python i18n libraries make you choose between **Babel + gettext** (powerful
but heavy, needs `.mo` compilation) or **hand-rolled dicts** (simple but no
plurals, no RTL, no fallback). `pyi18n-plug` sits in the middle:

- **Zero hard dependencies.** `pip install pyi18n-plug` gives you a working i18n
  engine. `babel` is optional and only activated for CLDR-exact plurals and
  number/currency/date formatting.
- **Plug in any language with plain JSON.** Drop a file in a folder, call
  `load_directory()`, done. No build step, no `.po` files, no `pybabel`.
- **Seven languages shipped out of the box:** English, German, French, Italian,
  Hindi, Urdu, Chinese — including **RTL detection** for Urdu.
- **Automatic fallback.** A missing key in `hi.json` falls through to English
  without crashing. Unknown placeholders stay literal so a broken translation
  never breaks the page.
- **CLI for everything.** `pyi18n demo`, `pyi18n list`, `pyi18n init es`,
  `pyi18n translate`, `pyi18n validate` — usable in CI.
- **Framework-agnostic.** Works in FastAPI, Flask, Django, scripts, bots,
  notebooks — anywhere Python runs.

---

## Installation

```bash
# Minimal — zero dependencies
pip install pyi18n-plug

# With optional CLDR formatting (plurals, numbers, currency, dates)
pip install "pyi18n-plug[babel]"