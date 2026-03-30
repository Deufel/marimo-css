import marimo

__generated_with = "0.21.1"
app = marimo.App()

with app.setup:
    import re
    from b_parse import find_properties, brace_depth
    from a_types import Issue


@app.function
def check_nested_properties(text: str, file: str) -> list[Issue]:
    """@property must sit at brace depth 0."""
    return [
        Issue(file, p["line"], "error",
              f"@property {p['name']} nested inside a block")
        for p in find_properties(text)
        if brace_depth(text, p["pos"]) > 0
    ]


@app.function
def check_hex_colors(text: str, file: str) -> list[Issue]:
    return [
        Issue(file, i, "warn", "raw hex color — use token?")
        for i, ln in enumerate(text.splitlines(), 1)
        if re.search(r'(?<!-)#[0-9a-fA-F]{3,8}\b', ln)
    ]


@app.function
def check_motion(text: str, file: str) -> list[Issue]:
    return [
        Issue(file, i, "error", "transition without --cfg-motion")
        for i, ln in enumerate(text.splitlines(), 1)
        if re.search(r'transition.*\d+(\.\d+)?s', ln) and '--cfg-motion' not in ln
    ]


@app.function
def check_undeclared_layers(declared: list[str], used: dict) -> list[Issue]:
    declared_set = set(declared)
    return [
        Issue(files[0], 0, "error", f"layer '{layer}' used but not declared")
        for layer, files in sorted(used.items())
        if layer not in declared_set
    ]


@app.function
def check_unused_layers(declared: list[str], used: dict) -> list[Issue]:
    return [
        Issue("", 0, "warn", f"layer '{layer}' declared but unused")
        for layer in declared
        if layer not in used
    ]


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
