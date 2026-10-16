# Spec MVP — Estatuto IBN da Paz (Akoma Ntoso + PDF)

## Contexto

O estatuto vigente da Igreja Batista Nacional da Paz de Guapó é um PDF escaneado (março/2002). O repositório mantém a fonte da verdade em Akoma Ntoso e gera PDF reproduzível.

## Objetivo

- Fonte da verdade: `akn/estatuto.xml` (Akoma Ntoso 3.0)
- Build local: validar XML → HTML → PDF em `dist/`
- Arquivar originais e referências normativas no Git

## Escopo

- Transcrição fiel do estatuto 2002 (correção só de OCR/encoding)
- Estrutura AKN com capítulos, artigos e parágrafos
- Scripts de validação e build
- PDFs em `sources/` e `refs/`

## Fora de escopo

- Reforma jurídica (Código Civil, LGPD, MROSC)
- Editor web
- Assinatura digital / LexML
- CI em nuvem

## Critérios de aceite

- [x] PDFs: `sources/estatuto-ibn-da-paz-2002.pdf`, `refs/codigo-civil-atualizado.pdf`, `refs/lgpd-1ed.pdf`, `refs/manual-mrosc-planejamento-prestacao-contas.pdf`
- [x] `akn/estatuto.xml` com Caps. I–V e Arts. 1–18
- [x] `python scripts/validate.py` OK
- [x] `python scripts/build.py` gera `dist/estatuto.html` e `dist/estatuto.pdf`
- [x] README com fluxo editar → validar → build

## Premissas

- Conteúdo jurídico permanece o de 2002
- Expressão FRBR: `2002-03-25`
- Referências em `refs/` não entram no build
