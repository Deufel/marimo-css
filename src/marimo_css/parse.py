import re

RE_PROPERTY_BLOCK = re.compile('@property\\s+(--[\\w-]+)\\s*\\{([^}]*)\\}')
RE_DESC_SYNTAX = re.compile('syntax:\\s*"([^"]*)"')
RE_DESC_INHERITS = re.compile('inherits:\\s*(true|false)')
RE_DESC_INITIAL = re.compile('initial-value:\\s*([^;]+)')
RE_LAYER_ORDER = re.compile('@layer\\s+([^;{]+);', re.DOTALL)
RE_LAYER_BLOCK = re.compile('@layer\\s+([\\w.:]+)\\s*\\{')
RE_VAR_DECL = re.compile('(--[\\w-]+)\\s*:')
RE_VAR_USE = re.compile('var\\((--[\\w-]+)')

def line_at(text: str, pos: int) -> int:
    return text[:pos].count('\n') + 1

def brace_depth(text: str, pos: int) -> int:
    return text[:pos].count('{') - text[:pos].count('}')

def find_properties(text: str) -> list[dict]:
    """Parse every @property block. Descriptors are read independently,
    so declaration order and spacing don't matter. A missing descriptor
    comes back as None — check_property_descriptors flags those."""
    props = []
    for m in RE_PROPERTY_BLOCK.finditer(text):
        name, body = m.group(1), m.group(2)
        syn = RE_DESC_SYNTAX.search(body)
        inh = RE_DESC_INHERITS.search(body)
        ini = RE_DESC_INITIAL.search(body)
        props.append(dict(
            name=name,
            syntax=syn.group(1) if syn else None,
            inherits=(inh.group(1) == "true") if inh else None,
            initial=ini.group(1).strip() if ini else None,
            line=line_at(text, m.start()), pos=m.start(),
        ))
    return props

def find_layer_order(text: str) -> list[str]:
    layers = []
    seen = set()
    for m in RE_LAYER_ORDER.finditer(text):
        raw = re.sub(r'/\*.*?\*/', '', m.group(1), flags=re.DOTALL)
        for name in raw.split(','):
            name = name.strip()
            if name and name not in seen:
                seen.add(name)
                layers.append(name)
    return layers

def find_layer_blocks(text: str) -> list[str]:
    return list(dict.fromkeys(RE_LAYER_BLOCK.findall(text)))

def find_var_decls(text: str) -> set[str]:
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    assigned   = set(RE_VAR_DECL.findall(text))
    propertied = {p["name"] for p in find_properties(text)}   # @property counts too
    return assigned | propertied

def find_var_refs(text: str) -> set[str]:
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    return set(RE_VAR_USE.findall(text))
