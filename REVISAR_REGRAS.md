# Mapa de revisão — Stage Area

A refatoração preserva os hardcodes, mas os tirou do meio do fluxo.

## 🔴 Revisar com prioridade

1. `stage_area/config.py`
   - `REGRAS_CLASSIFICACAO_PARCIAL`
   - `CORRECOES_CLASSIFICACAO`

Esses pontos representam exceções manuais explícitas no notebook.

## 🟠 Revisar depois

2. `SUB_EXCLUIDOS`
3. `ATIVOS_EXCLUIDOS`
4. `VALORES_AUSENTES`
5. `NORMALIZACOES_EXATAS`

Aqui vale validar se são regras permanentes ou correções históricas.

## 🟡 Revisar tecnicamente

6. Regra `Contenido` para `ML`/`GR`.
7. Representação de não classificação como `"o"`.
8. Uso do primeiro match em `buscar_valor()`.
9. Aplicação de `RuleMap` linha a linha com `DataFrame.apply()`.

## Observação

Não tentei "melhorar" as regras de negócio automaticamente. A intenção foi
primeiro tornar o processo legível e permitir que as regras sejam revisadas
sem precisar caçar células no notebook.
