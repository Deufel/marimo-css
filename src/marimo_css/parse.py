import re

RE_PROPERTY = re.compile('@property\\s+(--[\\w-]+)\\s*\\{\\s*syntax:\\s*"([^"]+)";\\s*inherits:\\s*(true|false);\\s*initial-value:\\s*([^;]+);\\s*\\}')
RE_LAYER_ORDER = re.compile('@layer\\s+([^;{]+);', re.DOTALL)
RE_LAYER_BLOCK = re.compile('@layer\\s+([\\w.:]+)\\s*\\{')
RE_VAR_DECL = re.compile('(--[\\w-]+)\\s*:')
RE_VAR_USE = re.compile('var\\((--[\\w-]+)')

def line_at(text: str, pos: int) -> int:
    return text[:pos].count('\n') + 1

def brace_depth(text: str, pos: int) -> int:
    return text[:pos].count('{') - text[:pos].count('}')

def find_properties(text: str) -> list[dict]:
    return [
        dict(name=m.group(1), syntax=m.group(2),
             inherits=m.group(3) == "true", initial=m.group(4).strip(),
             line=line_at(text, m.start()), pos=m.start())
        for m in RE_PROPERTY.finditer(text)
    ]

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
    return list(dict.fromkeys(RE_LAYER_BLOCK.findall(text)))  # dedup, preserve order

def find_var_decls(text: str) -> set[str]:
    return set(RE_VAR_DECL.findall(text))

def find_var_refs(text: str) -> set[str]:
    return set(RE_VAR_USE.findall(text))
