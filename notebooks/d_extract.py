import marimo

__generated_with = "0.21.1"
app = marimo.App()

with app.setup:
    import re
    from pathlib import Path


@app.function
def read_file(path: str) -> str:
    return Path(path).read_text()


@app.function
def extract_md_blocks(source: str) -> list[str]:
    pattern = r'mo\.md\(r"""\n(.*?)"""'
    return re.findall(pattern, source, flags=re.DOTALL)


@app.function
def extract_lang_blocks(blocks: list[str], lang: str) -> list[str]:
    pattern = rf'```{lang}\n(.*?)```'
    result = []
    for block in blocks:
        result.extend(re.findall(pattern, block, flags=re.DOTALL))
    return result


@app.function
def get_css(notebook_path: str) -> str:
    """Extract all CSS from a marimo notebook."""
    source = read_file(notebook_path)
    return "\n".join(extract_lang_blocks(extract_md_blocks(source), "css"))


@app.function
def find_notebooks(directory: str = "./notebooks") -> list[Path]:
    """Find all .py files in a directory."""
    d = Path(directory)
    return sorted(d.glob("*.py")) if d.exists() else []


@app.function
def export_one(notebook: Path, out_dir: Path = None) -> Path:
    """Extract CSS from one notebook → <name>.css. Returns output path."""
    css = get_css(str(notebook))
    dest = (out_dir or notebook.parent) / f"{notebook.stem}.css"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(css)
    return dest


@app.function
def export_all(directory: str = "./notebooks", out_dir: str = None) -> list[Path]:
    """Extract CSS from all notebooks in directory. Returns output paths."""
    notebooks = find_notebooks(directory)
    _out = Path(out_dir) if out_dir else None
    return [export_one(nb, _out) for nb in notebooks]


if __name__ == "__main__":
    app.run()
