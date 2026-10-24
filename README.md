# pyi18n-plug

> Lightweight, plugin-style internationalization for Python — JSON catalogs,
> CLDR plurals, RTL support, and a CLI. Zero hard dependencies.

[![PyPI version](https://img.shields.io/pypi/v/pyi18n-plug.svg)](https://pypi.org/project/pyi18n-plug/)
[![PyPI downloads](https://img.shields.io/pypi/dm/pyi18n-plug.svg)](https://pypi.org/project/pyi18n-plug/)
[![Python versions](https://img.shields.io/pypi/pyversions/pyi18n-plug.svg)](https://pypi.org/project/pyi18n-plug/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Publish to PyPI](https://github.com/ankitarora05/pyi18n-plug/actions/workflows/workflow.yml/badge.svg)](https://github.com/ankitarora05/pyi18n-plug/actions/workflows/workflow.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## Install

```bash
# Minimal — zero dependencies, works out of the box
pip install pyi18n-plug

# With optional CLDR formatting (plurals, numbers, currency, dates)
pip install "pyi18n-plug[babel]"
```

Requires **Python 3.9+**. No hard runtime dependencies.

---

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

## Verify the install

After installing, run the built-in demo — this proves the package, its CLI
entry point, and all seven bundled locale files are present and working:

```bash
pyi18n demo
```

Expected output (seven greetings, one per locale):

```
========================================================
pyi18n  demo  —  built-in locales
========================================================
Available: de, en, fr, hi, it, ur, zh

[de]
  t(greeting, name=World) -> Hallo, World!
  ...

[ur]
  t(greeting, name=World) -> ہیلو، World!
  ...
```

A one-liner check:

```bash
python -c "
import sys; sys.path.insert(0, 'src')
from pyi18n import I18n
i = I18n()
for loc in i.available_locales():
    i.set_locale(loc)
    print(loc, '->', i.t('greeting', name='World'))
"
# de -> Hallo, World!
# en -> Hello, World!
# fr -> Bonjour, World !
# hi -> नमस्ते, World!
# it -> Ciao, World!
# ur -> ہیلو، World!
# zh -> 你好，World！
```

---

## Quick start

```python
from pyi18n import I18n

i18n = I18n()                                 # English is active by default
print(i18n.t("greeting", name="World"))
# → Hello, World!

i18n.set_locale("hi")                         # switch to Hindi
print(i18n.t("greeting", name="दुनिया"))
# → नमस्ते, दुनिया!

i18n.set_locale("ur")                         # switch to Urdu (RTL)
print(i18n.t("greeting", name="دنیا"))
print(i18n.direction)                         # → 'rtl'
```

---

## Built-in locales

Seven languages ship with the package — usable immediately after `pip install`:

| Code | Language | Script     | Direction | Plural categories |
| ---- | -------- | ---------- | --------- | ----------------- |
| `en` | English  | Latin      | LTR       | `one`, `other`    |
| `de` | German   | Latin      | LTR       | `one`, `other`    |
| `fr` | French   | Latin      | LTR       | `one`, `other`    |
| `it` | Italian  | Latin      | LTR       | `one`, `other`    |
| `hi` | Hindi    | Devanagari | LTR       | `one`, `other`    |
| `ur` | Urdu     | Arabic     | **RTL**   | `one`, `other`    |
| `zh` | Chinese  | Han        | LTR       | `other`           |

Verify what's installed:

```python
from pyi18n import I18n
print(I18n().available_locales())
# → ['de', 'en', 'fr', 'hi', 'it', 'ur', 'zh']
```

---

## Adding your own languages

Three ways — pick whichever fits your workflow.

### 1. From an in-memory dictionary

```python
i18n.register_locale("es", data={
    "greeting": "Hola, {name}!",
    "welcome": "Bienvenido a pyi18n-plug.",
    "items": {"one": "{count} elemento", "other": "{count} elementos"},
})
i18n.set_locale("es")
print(i18n.t("greeting", name="Mundo"))   # → Hola, Mundo!
```

### 2. From a JSON file

```python
i18n.register_locale("pt", path="locales/pt.json")
```

### 3. From a whole folder

Point at a directory; every `*.json` file becomes a locale named after its
filename stem:

```python
loaded = i18n.load_directory("./locales")   # returns number of files loaded
print(f"Loaded {loaded} locales")
```

```
locales/
├── en.json     ← English (fallback)
├── es.json     ← Spanish
├── pt.json     ← Portuguese
└── sw.json     ← Swahili
```

### Catalog format

Every catalog is a nested JSON object. Placeholders use Python's
`str.format` syntax. Plural entries are objects whose keys are CLDR
categories:

```json
{
  "greeting": "Hello, {name}!",
  "welcome": "Welcome to pyi18n-plug.",
  "errors": {
    "not_found": "{name} was not found."
  },
  "items": {
    "one":   "{count} item",
    "other": "{count} items"
  }
}
```

Nested keys use dots — `i18n.t("errors.not_found", name="User")`.

---

## Plurals

Uses Babel's full CLDR rules when installed, with a safe fallback when not:

```python
i18n.set_locale("en")
i18n.plural("items", 1)     # → '1 item'
i18n.plural("items", 5)     # → '5 items'

i18n.set_locale("fr")
i18n.plural("items", 0)     # → '0 élément'    (French CLDR: 0 → one)
i18n.plural("items", 2)     # → '2 éléments'

i18n.set_locale("zh")
i18n.plural("items", 3)     # → '3 个项目'     (Chinese has only 'other')
```

Or let `t()` pick the form automatically:

```python
i18n.t("items", count=7)    # → '7 items'
```

---

## RTL support

```python
from pyi18n import is_rtl, RTL_LOCALES

is_rtl("ur")        # → True
is_rtl("he")        # → True
is_rtl("en")        # → False
RTL_LOCALES         # → frozenset({'ar', 'ur', 'he', 'fa', 'yi'})

i18n.set_locale("ur")
i18n.direction      # → 'rtl'
```

In templates: `<html lang="{{ i18n.locale }}" dir="{{ i18n.direction }}">`.

---

## CLI

After `pip install pyi18n-plug`, the `pyi18n` command is on your `PATH`:

```bash
# Print sample translations for every built-in locale
pyi18n demo

# List registered locales
pyi18n list

# Create a starter catalog — useful when adding a new language
pyi18n init es
# → wrote es.json

# Translate a key from the shell (great for debugging placeholders)
pyi18n translate greeting -l hi -p name=World
pyi18n translate items    -l en -p count=3

# CI check: reports any keys in en.json missing from other catalogs
pyi18n validate ./locales
```

Exit codes are `0` (success) / `1` (failure), so `validate` drops into CI
without any wrapper.

---

## Optional formatting (numbers, currency, dates)

Available with `pip install "pyi18n-plug[babel]"`. Each method falls back to
`str()` if Babel is not installed, so calling them is always safe.

```python
from datetime import datetime

i18n.set_locale("de")
i18n.number(1234.5)                    # → '1.234,5'
i18n.currency(99.99, "EUR")            # → '99,99 €'
i18n.datetime(datetime.now())          # → '24.10.2026, 14:03:22'

i18n.set_locale("hi")
i18n.number(1234567)                   # → '12,34,567'  (Indian grouping)
```

---

## Fallback chain

Missing keys never raise — they fall through in this order:

```
current locale → fallback locale → default (en) → literal key string
```

```python
i18n.register_locale("xx", {"greeting": "X {name}!"})
i18n.set_locale("xx")

i18n.t("greeting", name="A")   # → 'X A!'             (from xx)
i18n.t("welcome")              # → 'Welcome...'       (from en)
i18n.t("does.not.exist")       # → 'does.not.exist'   (literal key)
i18n.t("greeting")             # → 'X {name}!'        (missing placeholder preserved)
```

A half-translated catalog still renders. You can ship new languages
incrementally without breaking production pages.

---

## Framework integration

### FastAPI

```python
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pyi18n import I18n

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/{locale}/", response_class=HTMLResponse)
async def home(request: Request, locale: str):
    i18n = I18n()
    try:
        i18n.set_locale(locale)
    except Exception:
        i18n.set_locale("en")
    html = templates.get_template("home.html").render(
        request=request, i18n=i18n, locale=i18n.locale,
    )
    response = HTMLResponse(html)
    response.headers["Content-Language"] = i18n.locale
    return response
```

### Flask

```python
from flask import Flask, g, request
from pyi18n import I18n

app = Flask(__name__)

@app.before_request
def _i18n():
    i18n = I18n()
    try:
        i18n.set_locale(request.accept_languages.best_match(i18n.available_locales()))
    except Exception:
        pass
    g.i18n = i18n

@app.get("/")
def home():
    return g.i18n.t("greeting", name="World")
```

### Django

```python
from django.http import HttpResponse
from pyi18n import I18n

I18N = I18n()   # module-level, one engine per process

def home(request):
    I18N.set_locale(request.LANGUAGE_CODE or "en")
    return HttpResponse(I18N.t("greeting", name="World"))
```

---

## API reference

| Call | Returns | Notes |
| ---- | ------- | ----- |
| `I18n(default_locale="en")` | `I18n` | Loads built-in catalogs |
| `i18n.set_locale(code)` | `None` | Raises `LocaleNotFoundError` if unknown |
| `i18n.t(key, **params)` | `str` | Substitutes `{placeholders}` |
| `i18n.plural(key, count)` | `str` | Picks CLDR form |
| `i18n.has(key)` | `bool` | True if key resolves in the chain |
| `i18n.available_locales()` | `list[str]` | Sorted |
| `i18n.locale` / `i18n.direction` | `str` | `'en'` / `'ltr'` |
| `i18n.register_locale(code, data=…)` | `None` | In-memory |
| `i18n.register_locale(code, path=…)` | `None` | From JSON file |
| `i18n.load_directory(path)` | `int` | Number of files loaded |
| `i18n.unregister_locale(code)` | `None` | Safe if missing |
| `i18n.number` / `currency` / `datetime` | `str` | Optional Babel extras |
| `is_rtl(code)` | `bool` | Locale-level helper |

---

## Development

```bash
git clone https://github.com/ankitarora05/pyi18n-plug.git
cd pyi18n-plug
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
```

Run the bundled demo:

```bash
python examples/demo.py
```

Add a new built-in locale:

```bash
cp src/pyi18n/locales/en.json src/pyi18n/locales/es.json
# translate values, keep keys identical
# register in SUPPORTED (src/pyi18n/core.py)
pytest -q
```

---

## CI

Every push and pull request runs tests, validation, and build verification via
[`.github/workflows/workflow.yml`](.github/workflows/workflow.yml). Releases
are published to PyPI automatically on GitHub Release via Trusted Publishing
(no stored tokens).

---

## License

MIT — see [LICENSE](LICENSE).

---

## Contributing

Issues and PRs welcome at
[ankitarora05/pyi18n-plug](https://github.com/ankitarora05/pyi18n-plug).

1. Add a test for any new behaviour (`pytest -q` must pass).
2. If you add a built-in locale, include every key that exists in `en.json`.
3. Keep the import path stable (`pyi18n`).