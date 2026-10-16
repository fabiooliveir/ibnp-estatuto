# Estatuto — Igreja Batista Nacional da Paz de Guapó

Manutenção do estatuto associativo em [Akoma Ntoso](http://www.akomantoso.org/) 3.0, com geração de PDF.

## Fonte da verdade

Edite [`akn/estatuto.xml`](akn/estatuto.xml). O PDF gerado é artefato de build.

## Fluxo

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt

python scripts/validate.py
python scripts/build.py
```

Saídas:

| Artefato | Descrição |
|----------|-----------|
| `dist/estatuto.pdf` | Estatuto reformado (texto oficial) |
| `dist/alteracoes-reforma-cc-art54.pdf` | Resumo das mudanças — art. 54 CC |
| `dist/alteracoes-reforma-lgpd.pdf` | Resumo das mudanças — LGPD |
| `dist/alteracoes-reforma-mrosc.pdf` | Resumo das mudanças — MROSC |
| `docs/alteracoes-reforma-*.md` | Fontes dos documentos de alterações |

Expressão atual: reformas art. 54 do CC + LGPD + MROSC (2026-10-12). Original de 2002 em `sources/`.

### PDF no Windows

O build tenta, nesta ordem:

1. **WeasyPrint** (requer Pango/Cairo/GTK — ver [instalação](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows))
2. **Chrome ou Edge** em modo headless (`--print-to-pdf`), se instalados no sistema

Se ambos falharem, use `dist/estatuto.html` e imprima em PDF pelo navegador.

## Arquivos de origem e referência

| Caminho | Conteúdo |
|---------|----------|
| [`sources/estatuto-ibn-da-paz-2002.pdf`](sources/estatuto-ibn-da-paz-2002.pdf) | Estatuto original (escaneado, mar/2002) |
| [`refs/codigo-civil-atualizado.pdf`](refs/codigo-civil-atualizado.pdf) | Código Civil (referência; não usado no build) |
| [`refs/lgpd-1ed.pdf`](refs/lgpd-1ed.pdf) | LGPD (referência) |
| [`refs/manual-mrosc-planejamento-prestacao-contas.pdf`](refs/manual-mrosc-planejamento-prestacao-contas.pdf) | Manual MROSC (referência) |

## Specs

- [`specs/mvp.md`](specs/mvp.md) — pipeline AKN + PDF  
- [`specs/reforma-cc-art54.md`](specs/reforma-cc-art54.md) — reforma art. 54  
- [`specs/reforma-lgpd.md`](specs/reforma-lgpd.md) — reforma LGPD  
- [`specs/reforma-mrosc.md`](specs/reforma-mrosc.md) — reforma MROSC  

