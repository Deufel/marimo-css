import re

def strip_comments(css: str) -> str:
    return re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)

def strip_whitespace(css: str) -> str:
    css = strip_comments(css)
    css = re.sub(r'\s+', ' ', css)           # collapse runs
    css = re.sub(r'\s*([{}:;,])\s*', r'\1', css)  # trim around syntax
    css = re.sub(r';\}', '}', css)            # drop trailing semicolons
    return css.strip()

def minify(css: str) -> str:
    return strip_whitespace(css)
