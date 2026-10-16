#!/usr/bin/env python3
"""Validate AKN XML, emit HTML/PDF for estatuto + documento de alterações."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.request import pathname2url

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
CSS_PATH = ROOT / "build" / "styles.css"


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, check=True)


def _browser_exe() -> Path | None:
    candidates = [
        Path(os.environ.get("PROGRAMFILES", r"C:\Program Files"))
        / "Google/Chrome/Application/chrome.exe",
        Path(os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)"))
        / "Google/Chrome/Application/chrome.exe",
        Path(os.environ.get("LOCALAPPDATA", ""))
        / "Google/Chrome/Application/chrome.exe",
        Path(os.environ.get("PROGRAMFILES", r"C:\Program Files"))
        / "Microsoft/Edge/Application/msedge.exe",
        Path(os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)"))
        / "Microsoft/Edge/Application/msedge.exe",
    ]
    for path in candidates:
        if path.is_file():
            return path
    return None


def write_pdf(html_path: Path, pdf_path: Path) -> None:
    try:
        from weasyprint import HTML

        HTML(filename=str(html_path), base_url=str(html_path.parent)).write_pdf(
            str(pdf_path)
        )
        print(f"OK: {pdf_path.relative_to(ROOT)} (WeasyPrint)")
        return
    except Exception as exc:  # noqa: BLE001
        print(
            f"AVISO: WeasyPrint indisponível ({exc}). Tentando Chromium/Edge…",
            file=sys.stderr,
        )

    browser = _browser_exe()
    if browser is None:
        print("ERRO: Chrome/Edge não encontrado para fallback de PDF.", file=sys.stderr)
        sys.exit(1)

    file_url = "file:" + pathname2url(str(html_path.resolve()))
    cmd = [
        str(browser),
        "--headless=new",
        "--disable-gpu",
        f"--print-to-pdf={pdf_path.resolve()}",
        "--no-pdf-header-footer",
        file_url,
    ]
    print("+", " ".join(cmd))
    try:
        subprocess.run(cmd, cwd=ROOT, check=True)
    except Exception as exc:  # noqa: BLE001
        print(f"ERRO: fallback Chromium/Edge falhou: {exc}", file=sys.stderr)
        sys.exit(1)

    if not pdf_path.is_file():
        print(f"ERRO: PDF não gerado: {pdf_path}", file=sys.stderr)
        sys.exit(1)
    print(f"OK: {pdf_path.relative_to(ROOT)} (Chromium/Edge headless)")


def write_estatuto_html() -> Path:
    sys.path.insert(0, str(ROOT / "scripts"))
    from akn_to_html import transform  # noqa: WPS433

    DIST.mkdir(parents=True, exist_ok=True)
    css = CSS_PATH.read_text(encoding="utf-8")
    shutil.copy2(CSS_PATH, DIST / "styles.css")
    html = transform(ROOT / "akn" / "estatuto.xml", css_href="styles.css")
    html_embedded = html.replace(
        '<link rel="stylesheet" href="styles.css"/>',
        f"<style>\n{css}\n</style>",
    )
    out = DIST / "estatuto.html"
    out.write_text(html_embedded, encoding="utf-8")
    print(f"OK: {out.relative_to(ROOT)}")
    return out


def write_alteracoes_html(src_name: str, out_stem: str, title: str) -> Path:
    sys.path.insert(0, str(ROOT / "scripts"))
    from md_to_html import transform_md  # noqa: WPS433

    src = ROOT / "docs" / src_name
    out = DIST / f"{out_stem}.html"
    md = src.read_text(encoding="utf-8")
    out.write_text(transform_md(md, title=title), encoding="utf-8")
    print(f"OK: {out.relative_to(ROOT)}")
    return out


def main() -> None:
    run([sys.executable, str(ROOT / "scripts" / "validate.py")])
    estatuto_html = write_estatuto_html()
    alt_cc = write_alteracoes_html(
        "alteracoes-reforma-cc-art54.md",
        "alteracoes-reforma-cc-art54",
        "Alterações — Reforma art. 54 CC",
    )
    alt_lgpd = write_alteracoes_html(
        "alteracoes-reforma-lgpd.md",
        "alteracoes-reforma-lgpd",
        "Alterações — Reforma LGPD",
    )
    alt_mrosc = write_alteracoes_html(
        "alteracoes-reforma-mrosc.md",
        "alteracoes-reforma-mrosc",
        "Alterações — Reforma MROSC",
    )
    write_pdf(estatuto_html, DIST / "estatuto.pdf")
    write_pdf(alt_cc, DIST / "alteracoes-reforma-cc-art54.pdf")
    write_pdf(alt_lgpd, DIST / "alteracoes-reforma-lgpd.pdf")
    write_pdf(alt_mrosc, DIST / "alteracoes-reforma-mrosc.pdf")


if __name__ == "__main__":
    main()
