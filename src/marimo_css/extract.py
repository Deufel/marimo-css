import re
from pathlib import Path

def read_file(path: str) -> str:
    return Path(path).read_text()

def extract_md_blocks(source: str) -> list[str]:
    pattern = r'mo\.md\(r"""\n(.*?)"""'
    return re.findall(pattern, source, flags=re.DOTALL)

def extract_lang_blocks(blocks: list[str], lang: str) -> list[str]:
    pattern = rf'```{lang}\n(.*?)```'
    result = []
    for block in blocks:
        result.extend(re.findall(pattern, block, flags=re.DOTALL))
    return result

def get_css(notebook_path: str) -> str:
    """Extract all CSS from a marimo notebook."""
    source = read_file(notebook_path)
    blocks = extract_md_blocks(source)
    return "\n".join(extract_lang_blocks(blocks, "css"))

def export_css(notebook_path: str, out_path: str = "output.css") -> str:
    """Extract CSS from notebook → write to file. Returns path used."""
    css = get_css(notebook_path)
    _path = Path(out_path)
    _path.parent.mkdir(parents=True, exist_ok=True)
    _path.write_text(css)
    return str(_path)
