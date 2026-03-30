from pathlib import Path
from .types import Report

B, D, R, RE, YE, CY, GR = ( "\033[1m", "\033[2m", "\033[0m", "\033[31m", "\033[33m", "\033[36m", "\033[32m" )

def print_summary(report: Report, log_path: Path):
    _c = lambda n, zero=GR, bad=RE: f"{zero if n == 0 else bad}{n}{R}"
    print(f"  {D}@properties{R}  {CY}{len(report.properties)}{R}")
    print(f"  {D}layers{R}       {CY}{len(report.layers_declared)}{R}")
    print(f"  {D}lines{R}        {CY}{report.total_lines}{R}")
    print(f"  {D}size{R}         {CY}{report.total_bytes / 1024:.1f} kB{R}")
    print(f"  {D}warnings{R}     {_c(report.warns, bad=YE)}")
    print(f"  {D}errors{R}       {_c(report.errors)}")
    print(f"  {D}log{R}          {D}{log_path}{R}")

def write_log(report: Report, path: Path):
    lines = []

    lines.append("@PROPERTIES")
    for p in sorted(report.properties, key=lambda p: p["name"]):
        inh = "inherit" if p["inherits"] else "local"
        lines.append(f"  {p['name']:<22} {p['syntax']:<12} {inh}  = {p['initial']}  {p['file']}:{p['line']}")

    lines.append("\nLAYERS")
    used = report.layers_used
    for i, layer in enumerate(report.layers_declared):
        status = "✓" if layer in used else "✗"
        lines.append(f"  {i+1:>3}. {layer:<28} {status}")

    lines.append("\nVARIABLES")
    lines.append(f"  declared: {len(report.var_decls)}  referenced: {len(report.var_refs)}")
    unused = sorted(report.var_decls - report.var_refs)
    if unused:
        lines.append(f"  unreferenced: {', '.join(unused)}")

    lines.append("\nISSUES")
    for iss in sorted(report.issues, key=lambda i: (i.file, i.line)):
        tag = "ERR" if iss.level == "error" else "WRN"
        lines.append(f"  [{tag}] {iss.file}:{iss.line} {iss.msg}")
    if not report.issues:
        lines.append("  none")

    path.write_text("\n".join(lines))
