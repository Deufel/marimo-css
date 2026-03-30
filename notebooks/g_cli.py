import marimo

__generated_with = "0.21.1"
app = marimo.App()

with app.setup:

    import sys
    from pathlib import Path
    from d_extract import get_css
    from e_lint import lint_project, find_root, lint_file
    from f_output import print_summary, write_log
    from a_types import Report


@app.function
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


@app.function
def main():
    args = sys.argv[1:]

    # single notebook mode: css-lint notebook.py
    if args and args[0].endswith(".py"):
        report = lint_notebook(args[0])
        log_path = Path("css_lint.log")
    else:
        root = find_root()
        report = lint_project(root)
        log_path = root / "css_lint.log"

    write_log(report, log_path)
    print_summary(report, log_path)
    sys.exit(1 if report.errors else 0)


if __name__ == "__main__":
    app.run()
