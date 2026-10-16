#!/usr/bin/env python3
"""Validate akn/estatuto.xml: well-formed XML + structural rules."""

from __future__ import annotations

import sys
from pathlib import Path

from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
AKN_PATH = ROOT / "akn" / "estatuto.xml"
NS = {"akn": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"}
EXPECTED_CHAPTERS = 7
EXPECTED_ARTICLES = 29

REQUIRED_PHRASES = [
    # art. 54 CC
    ("organização religiosa", "art. 54, I — natureza"),
    ("demissão do quadro de membros", "art. 54, II — demissão"),
    ("justa causa", "art. 54, II / art. 57 — exclusão"),
    ("direito de defesa", "art. 57 — defesa"),
    ("São deveres dos membros", "art. 54, III — deveres"),
    ("fontes de recursos para a manutenção", "art. 54, IV"),
    ("órgão deliberativo máximo", "art. 54, V"),
    ("prestação de contas", "art. 54, VII — contas"),
    ("alteração das disposições estatutárias", "art. 54, VI — alteração"),
    # LGPD
    ("proteção de dados pessoais", "LGPD — capítulo"),
    ("controladora dos dados pessoais", "LGPD — controlador"),
    ("dados pessoais sensíveis", "LGPD — dados sensíveis"),
    ("direitos, inclusive confirmação", "LGPD — direitos do titular"),
    ("encarregado pelo tratamento", "LGPD — encarregado"),
    ("política de privacidade", "LGPD — política"),
    # MROSC
    ("interesse público e de cunho social", "MROSC — fins / art. 2º, I, c"),
    ("termos de colaboração", "MROSC — instrumentos"),
    ("escrituração de acordo com os princípios fundamentais de contabilidade", "MROSC — art. 33, IV"),
    ("Normas Brasileiras de Contabilidade", "MROSC — NBC"),
    ("Convenção Batista Nacional – Seção de Goiás", "MROSC — dissolução CBN preservada"),
]


def fail(msg: str) -> None:
    print(f"ERRO: {msg}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    if not AKN_PATH.is_file():
        fail(f"arquivo não encontrado: {AKN_PATH}")

    try:
        tree = etree.parse(str(AKN_PATH))
    except etree.XMLSyntaxError as exc:
        fail(f"XML malformado: {exc}")

    root = tree.getroot()
    if root.tag != "{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}akomaNtoso":
        fail(f"raiz esperada akomaNtoso, obtido: {root.tag}")

    chapters = root.xpath("//akn:body/akn:chapter", namespaces=NS)
    if len(chapters) != EXPECTED_CHAPTERS:
        fail(f"esperados {EXPECTED_CHAPTERS} capítulos, encontrados {len(chapters)}")

    articles = root.xpath("//akn:body//akn:article", namespaces=NS)
    if len(articles) != EXPECTED_ARTICLES:
        fail(f"esperados {EXPECTED_ARTICLES} artigos, encontrados {len(articles)}")

    eids = root.xpath("//akn:*[@eId]/@eId", namespaces=NS)
    if len(eids) != len(set(eids)):
        dupes = sorted({e for e in eids if eids.count(e) > 1})
        fail(f"eId duplicados: {', '.join(dupes)}")

    for i in range(1, EXPECTED_ARTICLES + 1):
        found = root.xpath(f"//akn:article[@eId='art_{i}']", namespaces=NS)
        if not found:
            fail(f"artigo ausente: art_{i}")

    for i in range(1, EXPECTED_CHAPTERS + 1):
        found = root.xpath(f"//akn:chapter[@eId='chp_{i}']", namespaces=NS)
        if not found:
            fail(f"capítulo ausente: chp_{i}")

    text = " ".join(root.xpath("//text()"))
    text_lower = text.casefold()
    for phrase, label in REQUIRED_PHRASES:
        if phrase.casefold() not in text_lower:
            fail(f"cobertura ausente ({label}): {phrase!r}")

    print(f"OK: {AKN_PATH.relative_to(ROOT)}")
    print(f"  capítulos: {len(chapters)}")
    print(f"  artigos:   {len(articles)}")
    print(f"  eIds:      {len(eids)} (únicos)")
    print(f"  checagens: {len(REQUIRED_PHRASES)} OK (art. 54 + LGPD + MROSC)")


if __name__ == "__main__":
    main()
