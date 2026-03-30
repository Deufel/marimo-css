import sys
from pathlib import Path
from .extract import get_css, export_all, find_notebooks
from .lint import lint_project, find_root, lint_file
from .output import print_summary, write_log
from .types import Report

USAGE = '    usage: css <command> [args]\n\n    commands:\n      extract   notebooks → css files     (default: ./notebooks/*.py)\n      lint      lint .css files            (default: project-wide)\n      check     extract + lint + cleanup   (default: ./notebooks/*.py)\n    '

def lint_notebook(notebook_path: str) -> Report:
    """Extract CSS from a marimo notebook and lint it."""
    css = get_css(notebook_path)
    # write to temp file so lint_file can reference it
    tmp = Path(notebook_path).with_suffix(".css")
    tmp.write_text(css)
    report = Report()
    lint_file(tmp, report, tmp.parent)
    tmp.unlink()
    return report

def cmd_extract(args: list[str]):
    directory = args[0] if args else "./notebooks"
    out_dir = args[1] if len(args) > 1 else None
    paths = export_all(directory, out_dir)
    for p in paths:
        print(f"  {p}")
    print(f"\n  {len(paths)} file{'s' * (len(paths) != 1)} extracted")

def cmd_lint(args: list[str]):
    if args and args[0].endswith(".css"):
        report = Report()
        p = Path(args[0])
        lint_file(p, report, p.parent)
    else:
        root = find_root()
        report = lint_project(root)

    log_path = Path("css_lint.log")
    write_log(report, log_path)
    print_summary(report, log_path)
    sys.exit(1 if report.errors else 0)

def cmd_check(args: list[str]):
    directory = args[0] if args else "./notebooks"
    notebooks = find_notebooks(directory)

    if not notebooks:
        print(f"  no notebooks found in {directory}")
        sys.exit(1)

    report = Report()
    tmp_files = []

    for nb in notebooks:
        css = get_css(str(nb))
        tmp = Path(f".tmp_{nb.stem}.css")
        tmp.write_text(css)
        tmp_files.append(tmp)
        lint_file(tmp, report, tmp.parent)

    for tmp in tmp_files:
        tmp.unlink()

    log_path = Path("css_lint.log")
    write_log(report, log_path)
    print_summary(report, log_path)
    sys.exit(1 if report.errors else 0)

def main():
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print(USAGE)
        sys.exit(0)

    cmd, rest = args[0], args[1:]

    commands = {
        "extract": cmd_extract,
        "lint": cmd_lint,
        "check": cmd_check,
    }

    if cmd not in commands:
        print(f"  unknown command: {cmd}\n")
        print(USAGE)
        sys.exit(1)

    commands[cmd](rest)
