import re
from .parse import find_properties, brace_depth
from .types import Issue

def check_property_descriptors(text: str, file: str) -> list[Issue]:
    """@property needs syntax, inherits, and initial-value to be valid CSS."""
    issues = []
    for p in find_properties(text):
        missing = [d for d, v in (("syntax", p["syntax"]),
                                  ("inherits", p["inherits"]),
                                  ("initial-value", p["initial"]))
                   if v is None]
        if missing:
            issues.append(Issue(file, p["line"], "error",
                f"@property {p['name']} missing: {', '.join(missing)}"))
    return issues

def check_nested_properties(text: str, file: str) -> list[Issue]:
    """@property must sit at brace depth 0."""
    return [
        Issue(file, p["line"], "error",
              f"@property {p['name']} nested inside a block")
        for p in find_properties(text)
        if brace_depth(text, p["pos"]) > 0
    ]

def check_hex_colors(text: str, file: str) -> list[Issue]:
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)   # skip comments
    return [
        Issue(file, i, "warn", "raw hex color — use a token?")
        for i, ln in enumerate(text.splitlines(), 1)
        if re.search(r'(?<![-\w])#[0-9a-fA-F]{3,8}\b', ln)
    ]

def check_motion(text: str, file: str) -> list[Issue]:
    return [
        Issue(file, i, "error", "transition without --cfg-motion")
        for i, ln in enumerate(text.splitlines(), 1)
        if re.search(r'transition.*\d+(\.\d+)?s', ln) and '--cfg-motion' not in ln
    ]

def check_undeclared_layers(declared: list[str], used: dict) -> list[Issue]:
    declared_set = set(declared)
    return [
        Issue(files[0], 0, "error", f"layer '{layer}' used but not declared")
        for layer, files in sorted(used.items())
        if layer not in declared_set
    ]

def check_unused_layers(declared: list[str], used: dict) -> list[Issue]:
    return [
        Issue("", 0, "warn", f"layer '{layer}' declared but unused")
        for layer in declared
        if layer not in used
    ]

def check_undeclared_vars(decls: set, refs: set) -> list[Issue]:
    """var(--x) where --x is never declared anywhere — usually a typo."""
    return [
        Issue("", 0, "warn", f"variable '{v}' used but never declared")
        for v in sorted(refs - decls)
    ]
