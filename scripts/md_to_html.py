#!/usr/bin/env python3
"""Minimal Markdown → HTML for the alterations presentation doc."""

from __future__ import annotations

import html
import re
from pathlib import Path


def _inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    text = re.sub(r"> (.+)$", r"\1", text)  # leftover
    return text


def transform_md(md: str, title: str = "Documento") -> str:
    lines = md.splitlines()
    body: list[str] = []
    i = 0
    in_ul = False
    in_table = False

    def close_ul() -> None:
        nonlocal in_ul
        if in_ul:
            body.append("</ul>")
            in_ul = False

    def close_table() -> None:
        nonlocal in_table
        if in_table:
            body.append("</tbody></table>")
            in_table = False

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped == "---":
            close_ul()
            close_table()
            body.append("<hr/>")
            i += 1
            continue

        if stripped.startswith("|") and "|" in stripped[1:]:
            close_ul()
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            # separator row
            if all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells):
                i += 1
                continue
            if not in_table:
                body.append('<table class="doc-table"><thead><tr>')
                body.append("".join(f"<th>{_inline(c)}</th>" for c in cells))
                body.append("</tr></thead><tbody>")
                in_table = True
                i += 1
                continue
            body.append("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in cells) + "</tr>")
            i += 1
            continue

        close_table()

        if stripped.startswith("# "):
            close_ul()
            body.append(f"<h1>{_inline(stripped[2:])}</h1>")
        elif stripped.startswith("## "):
            close_ul()
            body.append(f"<h2>{_inline(stripped[3:])}</h2>")
        elif stripped.startswith("> "):
            close_ul()
            quote = stripped[2:]
            # gather continuation
            i += 1
            while i < len(lines) and lines[i].startswith("> "):
                quote += " " + lines[i][2:]
                i += 1
            body.append(f"<blockquote><p>{_inline(quote)}</p></blockquote>")
            continue
        elif re.match(r"^[-*] ", stripped):
            if not in_ul:
                body.append("<ul>")
                in_ul = True
            body.append(f"<li>{_inline(stripped[2:])}</li>")
        elif re.match(r"^\d+\. ", stripped):
            close_ul()
            # start or continue ol — simple: each numbered as paragraph list via ol open/close per block
            if not body or not body[-1].startswith("<ol") and "</ol>" not in "".join(body[-3:]):
                # open ol if previous wasn't ol item
                if not (len(body) >= 1 and body[-1].startswith("<li>") and "<ol>" in "".join(body[-5:])):
                    pass
            # simpler approach: use ul-style with number in text, or proper ol
            if not (body and any(x == "<ol>" for x in body[-8:])):
                # check if last open was ol
                open_ol = sum(1 for b in body if b == "<ol>") - sum(1 for b in body if b == "</ol>")
                if open_ol <= 0:
                    body.append("<ol>")
            item = re.sub(r"^\d+\. ", "", stripped)
            body.append(f"<li>{_inline(item)}</li>")
            # peek next
            if i + 1 >= len(lines) or not re.match(r"^\d+\. ", lines[i + 1].strip()):
                body.append("</ol>")
        elif stripped == "":
            close_ul()
        else:
            close_ul()
            body.append(f"<p>{_inline(stripped)}</p>")
        i += 1

    close_ul()
    close_table()
    # close dangling ol
    if sum(1 for b in body if b == "<ol>") > sum(1 for b in body if b == "</ol>"):
        body.append("</ol>")

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{html.escape(title)}</title>
  <style>
@page {{ size: A4; margin: 2cm; }}
body {{
  font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
  font-size: 11pt;
  line-height: 1.45;
  color: #1a1a1a;
  max-width: 48rem;
  margin: 0 auto;
  padding: 1rem 1.25rem 2rem;
}}
h1 {{ font-size: 1.45rem; margin-top: 0; }}
h2 {{ font-size: 1.15rem; margin-top: 1.5rem; border-bottom: 1px solid #ccc; padding-bottom: 0.25rem; }}
blockquote {{
  margin: 1rem 0;
  padding: 0.6rem 1rem;
  background: #f5f5f5;
  border-left: 3px solid #444;
}}
table.doc-table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
  margin: 0.75rem 0 1.25rem;
}}
table.doc-table th, table.doc-table td {{
  border: 1px solid #bbb;
  padding: 0.4rem 0.5rem;
  vertical-align: top;
  text-align: left;
}}
table.doc-table th {{ background: #eee; }}
hr {{ border: none; border-top: 1px solid #ccc; margin: 1.5rem 0; }}
code {{ font-size: 0.9em; }}
  </style>
</head>
<body>
{chr(10).join(body)}
</body>
</html>
"""


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    src = root / "docs" / "alteracoes-reforma-cc-art54.md"
    out = root / "dist" / "alteracoes-reforma-cc-art54.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    md = src.read_text(encoding="utf-8")
    out.write_text(
        transform_md(md, title="Alterações — Reforma art. 54 CC"),
        encoding="utf-8",
    )
    print(f"OK: {out.relative_to(root)}")


if __name__ == "__main__":
    main()
