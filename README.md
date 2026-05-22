# marimo-css
![PyPI version](https://img.shields.io/pypi/v/marimo-css)


> [!WARNING]
> This is an opinonated personal tool not an official marimo tool - May 2026.

pypi names are forever

Write CSS in a marimo notebook — then extract, lint*, and minify it.

*opinonated checks

## Install

```bash
pip install marimo-css
```

## Commands

```bash
css extract            # notebooks → css files
css extract --min      # extract, then minify
css lint               # lint .css files (project-wide)
css lint path/to.css   # lint one file
css minify file.css    # strip comments + whitespace → stdout
css check              # extract + lint in one pass
```

`extract`, `check` default to `./notebooks/*.py`. `lint` defaults to the
whole project — it finds the root by walking up to `pyproject.toml`.

## What the linter checks

Per file:

- `@property` blocks are at the top level, not nested in a rule
- `@property` blocks declare all three descriptors — `syntax`,
  `inherits`, `initial-value`
- no raw hex colors — prefer a token
- every `transition` with a time value routes through `--cfg-motion`

Project-wide:

- every `@layer` used in a block is also declared in the layer order
- layers declared but never used
- custom properties: declared & used, declared but never used, and
  used but never declared (the last usually means a typo)

Errors exit non-zero; warnings don't. Full results are written to
`css_lint.log`.

## Exit codes

`0` clean or warnings only · `1` one or more errors.