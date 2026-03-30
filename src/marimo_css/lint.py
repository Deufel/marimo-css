from pathlib import Path
from .types import Report
from .parse import find_properties, find_layer_order, find_layer_blocks, find_var_decls, find_var_refs
from .rules import check_undeclared_layers, check_unused_layers, check_hex_colors, check_motion, check_nested_properties

ALL_RULES = [check_nested_properties, check_hex_colors, check_motion]
SKIP = {'.venv', 'node_modules', 'dist'}

def should_skip(path: Path, root: Path) -> bool:
    rel = str(path.relative_to(root))
    return any(rel.startswith(s) for s in SKIP)

def find_root(start: Path = None, marker: str = "pyproject.toml") -> Path:
    p = (start or Path.cwd()).resolve()
    for parent in [p, *p.parents]:
        if (parent / marker).exists():
            return parent
    raise FileNotFoundError(f"No {marker} above {p}")

def lint_file(path: Path, report: Report, root: Path):
    rel = str(path.relative_to(root))
    text = path.read_text()

    report.total_lines += text.count('\n') + 1
    report.total_bytes += path.stat().st_size

    report.properties.extend(
        {**p, "file": rel} for p in find_properties(text)
    )

    order = find_layer_order(text)
    if order:
        report.layers_declared.extend(order)

    for name in find_layer_blocks(text):
        report.layers_used[name].append(rel)

    report.var_decls |= find_var_decls(text)
    report.var_refs |= find_var_refs(text)

    for rule in ALL_RULES:
        report.issues.extend(rule(text, rel))

def lint_project(root: Path = None) -> Report:
    root = root or find_root()
    report = Report()

    for path in sorted(root.rglob("*.css")):
        if not should_skip(path, root):
            lint_file(path, report, root)

    report.issues.extend(check_undeclared_layers(report.layers_declared, report.layers_used))
    report.issues.extend(check_unused_layers(report.layers_declared, report.layers_used))

    return report
