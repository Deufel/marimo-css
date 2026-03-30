import marimo

__generated_with = "0.21.1"
app = marimo.App()

with app.setup:
    from pathlib import Path
    from a_types import Report
    from b_parse import (find_properties, find_layer_order, find_layer_blocks,
                        find_var_decls, find_var_refs)
    from c_rules import check_undeclared_layers, check_unused_layers, check_hex_colors, check_motion, check_nested_properties

    ALL_RULES = [check_nested_properties, check_hex_colors, check_motion]
    SKIP = {".venv", "node_modules", "dist"}



@app.function
def should_skip(path: Path, root: Path) -> bool:
    rel = str(path.relative_to(root))
    return any(rel.startswith(s) for s in SKIP)


@app.function
def find_root(start: Path = None, marker: str = "pyproject.toml") -> Path:
    p = (start or Path.cwd()).resolve()
    for parent in [p, *p.parents]:
        if (parent / marker).exists():
            return parent
    raise FileNotFoundError(f"No {marker} above {p}")


@app.function
def lint_file(path: Path, report: Report, root: Path):
    rel = str(path.relative_to(root))
    text = path.read_text()

    # stats
    report.total_lines += text.count('\n') + 1
    report.total_bytes += path.stat().st_size

    # properties
    report.properties.extend({**p, "file": rel} for p in find_properties(text))

    # layers — dedup into report
    for layer in find_layer_order(text):
        if layer not in report.layers_declared:
            report.layers_declared.append(layer)

    for name in find_layer_blocks(text):
        if rel not in report.layers_used.get(name, []):
            report.layers_used[name].append(rel)

    # variables
    report.var_decls |= find_var_decls(text)
    report.var_refs |= find_var_refs(text)

    # rules
    for rule in ALL_RULES:
        report.issues.extend(rule(text, rel))


@app.function
def lint_project(root: Path = None) -> Report:
    root = root or find_root()
    report = Report()

    for path in sorted(root.rglob("*.css")):
        if not should_skip(path, root):
            lint_file(path, report, root)

    report.issues.extend(check_undeclared_layers(report.layers_declared, report.layers_used))
    report.issues.extend(check_unused_layers(report.layers_declared, report.layers_used))

    return report


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
