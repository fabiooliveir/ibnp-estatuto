#!/usr/bin/env python3
"""Transform Akoma Ntoso estatuto XML into printable HTML."""

from __future__ import annotations

import html
from pathlib import Path

from lxml import etree

NS = {"akn": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"}


def _text(el: etree._Element | None) -> str:
    if el is None:
        return ""
    return " ".join("".join(el.itertext()).split())


def _p_html(container: etree._Element | None) -> str:
    if container is None:
        return ""
    parts: list[str] = []
    for p in container.xpath("./akn:p", namespaces=NS):
        parts.append(f"<p>{html.escape(_text(p))}</p>")
    if not parts:
        t = _text(container)
        if t:
            parts.append(f"<p>{html.escape(t)}</p>")
    return "\n".join(parts)


def _render_points(parent: etree._Element) -> str:
    points = parent.xpath("./akn:point", namespaces=NS)
    if not points:
        return ""
    items: list[str] = []
    for point in points:
        num = _text(point.find("akn:num", NS))
        body = _p_html(point.find("akn:content", NS))
        items.append(
            f'<li class="point"><span class="num">{html.escape(num)}</span> {body}</li>'
        )
    return '<ol class="points">' + "\n".join(items) + "</ol>"


def _render_paragraphs(article: etree._Element) -> str:
    out: list[str] = []
    for para in article.xpath("./akn:paragraph", namespaces=NS):
        num = _text(para.find("akn:num", NS))
        eid = para.get("eId", "")
        intro = _p_html(para.find("akn:intro", NS))
        content = _p_html(para.find("akn:content", NS))
        points = _render_points(para)
        out.append(
            f'<section class="paragraph" id="{html.escape(eid)}">'
            f'<h4 class="para-num">{html.escape(num)}</h4>'
            f"{intro}{content}{points}"
            f"</section>"
        )
    return "\n".join(out)


def _render_article(article: etree._Element) -> str:
    eid = article.get("eId", "")
    num = _text(article.find("akn:num", NS))
    heading = _text(article.find("akn:heading", NS))
    intro = _p_html(article.find("akn:intro", NS))
    content = _p_html(article.find("akn:content", NS))
    points = _render_points(article)
    paragraphs = _render_paragraphs(article)
    heading_html = f"<p class='article-heading'>{html.escape(heading)}</p>" if heading else ""
    return (
        f'<article class="article" id="{html.escape(eid)}">'
        f"<h3>{html.escape(num)}</h3>"
        f"{heading_html}{intro}{content}{points}{paragraphs}"
        f"</article>"
    )


def transform(xml_path: Path, css_href: str = "../build/styles.css") -> str:
    tree = etree.parse(str(xml_path))
    root = tree.getroot()

    title = _text(root.find(".//akn:docTitle", NS)) or "Estatuto"
    authority = _text(root.find(".//akn:docAuthority", NS))
    doc_date = _text(root.find(".//akn:docDate", NS))

    chapters_html: list[str] = []
    for chapter in root.xpath("//akn:body/akn:chapter", namespaces=NS):
        eid = chapter.get("eId", "")
        num = _text(chapter.find("akn:num", NS))
        heading = _text(chapter.find("akn:heading", NS))
        arts = "\n".join(
            _render_article(a) for a in chapter.xpath("./akn:article", namespaces=NS)
        )
        chapters_html.append(
            f'<section class="chapter" id="{html.escape(eid)}">'
            f"<h2>{html.escape(num)} — {html.escape(heading)}</h2>"
            f"{arts}"
            f"</section>"
        )

    conclusions = root.find(".//akn:conclusions", NS)
    conclusions_html = ""
    if conclusions is not None:
        blocks = [_p_html(conclusions)]
        # conclusions may have multiple p directly
        ps = [
            f"<p>{html.escape(_text(p))}</p>"
            for p in conclusions.xpath("./akn:p", namespaces=NS)
        ]
        conclusions_html = (
            '<section class="conclusions"><h2>Fecho</h2>'
            + ("\n".join(ps) if ps else "".join(blocks))
            + "</section>"
        )

    body = "\n".join(chapters_html) + conclusions_html

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{html.escape(title)} — {html.escape(authority)}</title>
  <link rel="stylesheet" href="{html.escape(css_href)}"/>
</head>
<body>
  <header class="cover">
    <p class="authority">{html.escape(authority)}</p>
    <h1>{html.escape(title)}</h1>
    <p class="date">{html.escape(doc_date)}</p>
    <p class="meta">Transcrição Akoma Ntoso — expressão 2002-03-25</p>
  </header>
  <main>
{body}
  </main>
</body>
</html>
"""


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    xml_path = root / "akn" / "estatuto.xml"
    out = root / "dist" / "estatuto.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(transform(xml_path, css_href="../build/styles.css"), encoding="utf-8")
    print(f"OK: {out.relative_to(root)}")


if __name__ == "__main__":
    main()
