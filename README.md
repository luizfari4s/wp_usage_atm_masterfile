# Stage Area — refatorado

Refatoração do notebook `stage_area.ipynb`.

## Objetivo

Separar a execução em camadas sem alterar deliberadamente a essência
das regras existentes.

### Estrutura

- `config.py`
  - concentra os hardcodes e exceções conhecidas;
  - é o primeiro lugar para revisar regras.

- `carregamento.py`
  - somente leitura das bases.

- `normalizacao.py`
  - limpeza e normalização da MF.

- `regras.py`
  - lógica de RuleMap;
  - divisão RBC 1:1 / não única;
  - classificação de novos/antigos;
  - resolução dos casos parciais.

- `pipeline.py`
  - orquestração do processo;
  - ponto que deve ser chamado pela Central.

- `main.py`
  - exemplo de execução.

## Onde revisar primeiro

### 1. Regras hardcoded de classificação parcial

`config.py`:

```python
REGRAS_CLASSIFICACAO_PARCIAL
```

Hoje existem os IdProd:

- 200 -> Clas01
- 63 -> Clas02
- 686 -> Sub
- 201 -> Sub
- 58 -> Sub
- 287 -> Producto
- 212 -> Sub
- 622 -> Sub
- 269 -> Clas02

Isso veio diretamente do notebook e deve ser tratado como dívida técnica/regra de negócio a revisar.

### 2. Correções manuais

`config.py`:

```python
CORRECOES_CLASSIFICACAO
```

São exceções textuais que estavam dentro da função original.

### 3. Filtros da MF

`config.py`:

```python
SUB_EXCLUIDOS
ATIVOS_EXCLUIDOS
```

Aqui está o filtro grande de `Codebook OOH...` e `Activo == AR`.

### 4. Normalização

`config.py`:

```python
VALORES_AUSENTES
NORMALIZACOES_EXATAS
```

São transformações que podem representar regra de negócio e não apenas limpeza técnica.

### 5. Regra STR -> ml/gr

`normalizacao.py`

A lógica de `Contenido` foi preservada, mas marcada para revisão.

## Integração com o orquestrador

O projeto não extrai ZIPs.

O orquestrador pode:

1. receber os arquivos;
2. extrair os ZIPs;
3. identificar os XLSX/CSVs;
4. chamar `processar_stage_area()`.

Isso deixa o processo independente da origem dos arquivos.
