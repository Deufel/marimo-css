import marimo

__generated_with = "0.21.1"
app = marimo.App()

with app.setup:
    import re

    RE_PROPERTY = re.compile(
        r'@property\s+(--[\w-]+)\s*\{'
        r'\s*syntax:\s*"([^"]+)";\s*'
        r'inherits:\s*(true|false);\s*'
        r'initial-value:\s*([^;]+);\s*\}'
    )
    RE_LAYER_ORDER = re.compile(r'@layer\s+([\w.:,\s/*-]+);', re.DOTALL)
    RE_LAYER_BLOCK = re.compile(r'@layer\s+([\w.:]+)\s*\{')
    RE_VAR_DECL = re.compile(r'(--[\w-]+)\s*:')
    RE_VAR_USE = re.compile(r'var\((--[\w-]+)')


@app.function
def line_at(text: str, pos: int) -> int:
    return text[:pos].count('\n') + 1


@app.function
def brace_depth(text: str, pos: int) -> int:
    return text[:pos].count('{') - text[:pos].count('}')


@app.function
def find_properties(text: str) -> list[dict]:
    return [
        dict(name=m.group(1), syntax=m.group(2),
             inherits=m.group(3) == "true", initial=m.group(4).strip(),
             line=line_at(text, m.start()), pos=m.start())
        for m in RE_PROPERTY.finditer(text)
    ]


@app.function
def find_layer_order(text: str) -> list[str]:
    layers = []
    for m in RE_LAYER_ORDER.finditer(text):
        raw = re.sub(r'/\*.*?\*/', '', m.group(1), flags=re.DOTALL)
        layers.extend(name.strip() for name in raw.split(',') if name.strip())
    return layers


@app.function
def find_layer_blocks(text: str) -> list[str]:
    return RE_LAYER_BLOCK.findall(text)


@app.function
def find_var_decls(text: str) -> set[str]:
    return set(RE_VAR_DECL.findall(text))


@app.function
def find_var_refs(text: str) -> set[str]:
    return set(RE_VAR_USE.findall(text))


if __name__ == "__main__":
    app.run()
