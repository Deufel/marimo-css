import marimo

__generated_with = "0.21.1"
app = marimo.App()

with app.setup:
    import re





@app.function
def strip_comments(css: str) -> str:
    return re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)


@app.function
def strip_whitespace(css: str) -> str:
    css = strip_comments(css)
    css = re.sub(r'\s+', ' ', css)           # collapse runs
    css = re.sub(r'\s*([{}:;,])\s*', r'\1', css)  # trim around syntax
    css = re.sub(r';\}', '}', css)            # drop trailing semicolons
    return css.strip()


@app.function
def minify(css: str) -> str:
    return strip_whitespace(css)


if __name__ == "__main__":
    app.run()
