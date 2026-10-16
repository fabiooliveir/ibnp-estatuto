# Spec — Reforma do estatuto (art. 54 do Código Civil)

## Contexto

O estatuto vigente (expressão 2002) não cobre de forma completa o conteúdo mínimo do art. 54 do CC. A igreja é organização religiosa (CC art. 44, IV e §1º); esta reforma alinha o estatuto aos incisos I–VII do art. 54, com o mínimo do art. 57 na exclusão.

## Objetivo

1. Nova expressão em `akn/estatuto.xml` + `dist/estatuto.pdf`
2. Documento de apresentação `docs/alteracoes-reforma-cc-art54.md` + `dist/alteracoes-reforma-cc-art54.pdf`

## Escopo / fora de escopo

- **Escopo:** art. 54 I–VII; art. 57 mínimo (exclusão)
- **Fora:** arts. 55–61 amplos; LGPD; MROSC; mudança de sede; parecer externo

## Matriz art. 54 → estatuto reformado

| Inciso | Exigência | Cobertura no estatuto |
|--------|-----------|------------------------|
| I | Denominação, fins e sede | Art. 1º; fins no art. 2º, § 4º |
| II | Admissão, demissão e exclusão | Arts. 3º (§ 1º), 4º e 5º |
| III | Direitos e deveres | Art. 3º, §§ 2º a 4º |
| IV | Fontes de recursos | Art. 11 |
| V | Órgãos deliberativos | Arts. 7º a 9º |
| VI | Alteração e dissolução | Arts. 25, 26 e 28 (Cap. VII — Disposições Gerais) |
| VII | Gestão administrativa e aprovação das contas | Arts. 9º, § 1º; 10, §§ 8º e 9º |

## Critérios de aceite

- [x] Matriz acima refletida no XML
- [x] Demissão voluntária (art. 4º)
- [x] Exclusão com justa causa, defesa e recurso (art. 5º)
- [x] Deveres expressos (art. 3º, § 4º)
- [x] Aprovação anual das contas (arts. 9º e 10)
- [x] Documento de alterações + PDF
- [x] `validate.py` e `build.py` OK
- [x] Original 2002 em `sources/`

## Nota

Documento de trabalho interno — não substitui advogado nem registro cartorial.
