from __future__ import annotations

import pandas as pd

from .config import (
    RESULTADO_RBC,
    RESULTADO_HISTORICO,
    RESULTADO_PARCIAL,
    RESULTADO_CONFLITO,
    RESULTADO_PARCIAL_RESOLVIDA,
    VALOR_NAO_CLASSIFICADO,
    REGRAS_CLASSIFICACAO_PARCIAL,
    CORRECOES_CLASSIFICACAO,
)


def separar_rbc_por_unicidade(rbc: dict):
    """
    Divide cada RBC entre correspondências 1:1 e não únicas.
    """
    unicas = {}
    nao_unicas = {}

    for nivel, tabela in rbc.items():
        contagem = tabela["IdProd"].value_counts().reset_index()
        contagem.columns = ["IdProd", "count"]

        ids_unicos = contagem.loc[
            contagem["count"] == 1,
            "IdProd",
        ]

        unicas[nivel] = tabela.loc[
            tabela["IdProd"].isin(ids_unicos)
        ].copy()

        nao_unicas[nivel] = tabela.loc[
            ~tabela["IdProd"].isin(ids_unicos)
        ].copy()

    return unicas, nao_unicas


def ids_nao_classificaveis(nao_unicas: dict) -> pd.DataFrame:
    tabelas = [
        df[["IdProd"]].copy()
        for df in nao_unicas.values()
    ]

    resultado = pd.concat(tabelas, ignore_index=True)
    resultado = resultado.drop_duplicates(subset=["IdProd"])
    resultado["IdProd"] = pd.to_numeric(
        resultado["IdProd"],
        errors="coerce",
    ).astype("Int64")

    return resultado


def aplicar_regra(id_produto, rule_table, row):
    """Monta DescUsage conforme RuleMap do produto."""
    regra_row = rule_table.loc[
        rule_table["IdProd"] == id_produto,
        "RuleMap",
    ]

    if regra_row.empty:
        return "Sem regra no dicionário"

    regra = regra_row.iloc[0]
    tokens = [token.strip() for token in regra.split("+")]

    valores = [
        str(row[token])
        for token in tokens
        if token in row.index and pd.notna(row[token])
    ]

    return " ".join(valores)


def aplicar_rbc(df, rule_table):
    df = df.copy()

    df["DescUsage"] = df.apply(
        lambda row: aplicar_regra(
            row["IdProd"],
            rule_table,
            row,
        ),
        axis=1,
    )

    df["DescUsage"] = df["DescUsage"].str.replace(
        "\u00A0",
        " ",
        regex=False,
    )

    return df


def juntar_niveis(df, level_data):
    merged = df.merge(
        level_data,
        on="IdArtigo",
        how="left",
    )

    merged = merged.dropna(axis=1, how="all")

    primeiras = [
        coluna
        for coluna in [
            "DescUsage",
            "NIVEL_1",
            "NIVEL_2",
            "NIVEL_3",
            "NIVEL_4",
        ]
        if coluna in merged.columns
    ]

    resto = [
        coluna
        for coluna in merged.columns
        if coluna not in primeiras
    ]

    merged = merged[primeiras + resto]

    for nivel in ["NIVEL_1", "NIVEL_2", "NIVEL_3", "NIVEL_4"]:
        if nivel in merged.columns:
            merged[nivel] = merged[nivel].fillna(VALOR_NAO_CLASSIFICADO)

    return merged


def classificar_produtos_novos(
    merged,
    rbc_unicas,
    nao_classificaveis,
):
    novos = merged.loc[
        merged["NIVEL_1"] == VALOR_NAO_CLASSIFICADO
    ].copy()

    novos = novos.drop(
        columns=["NIVEL_1", "NIVEL_2", "NIVEL_3", "NIVEL_4"]
    )

    antigos = merged.loc[
        merged["NIVEL_1"] != VALOR_NAO_CLASSIFICADO
    ].copy()

    for nivel in ["N1", "N2", "N3", "N4"]:
        novos = novos.merge(
            rbc_unicas[nivel],
            on="IdProd",
            how="left",
        )

    # A ordem das colunas não deve ser tratada como regra de negócio.
    primeiras = [
        coluna
        for coluna in [
            "DescUsage",
            "NIVEL_1",
            "NIVEL_2",
            "NIVEL_3",
            "NIVEL_4",
        ]
        if coluna in novos.columns
    ]
    resto = [c for c in novos.columns if c not in primeiras]
    novos = novos[primeiras + resto]

    for nivel in ["NIVEL_1", "NIVEL_2", "NIVEL_3", "NIVEL_4"]:
        novos[nivel] = novos[nivel].fillna(VALOR_NAO_CLASSIFICADO)

    conflitos = novos.loc[
        (novos["NIVEL_1"] == VALOR_NAO_CLASSIFICADO)
        & (novos["NIVEL_2"] == VALOR_NAO_CLASSIFICADO)
        & (novos["NIVEL_3"] == VALOR_NAO_CLASSIFICADO)
        & (novos["NIVEL_4"] == VALOR_NAO_CLASSIFICADO)
    ]["IdArtigo"]

    partial_ids = novos.loc[
        novos["IdProd"].isin(nao_classificaveis["IdProd"])
    ]["IdArtigo"]

    novos["Result"] = RESULTADO_RBC
    novos.loc[
        novos["IdArtigo"].isin(partial_ids),
        "Result",
    ] = RESULTADO_PARCIAL
    novos.loc[
        novos["IdArtigo"].isin(conflitos),
        "Result",
    ] = RESULTADO_CONFLITO

    antigos["Result"] = RESULTADO_HISTORICO

    return antigos, novos


def buscar_valor(df, coluna, termo):
    """
    Retorna o primeiro valor da coluna que contém o termo.
    Mantém o comportamento original do notebook.
    """
    if coluna not in df.columns:
        return VALOR_NAO_CLASSIFICADO

    mask = df[coluna].astype(str).str.contains(
        str(termo),
        case=False,
        na=False,
    )

    resultados = df.loc[mask, coluna].values

    if len(resultados) == 0:
        return VALOR_NAO_CLASSIFICADO

    return str(resultados[0])


def resolver_classificacao_parcial(
    filter_df,
    target_df,
    rbc_nao_unicas,
):
    """
    Resolve os casos parciais usando as regras individuais antigas.

    >>> REVISAR AQUI
    O dicionário REGRAS_CLASSIFICACAO_PARCIAL em config.py
    concentra os IdProd hardcoded.
    """
    target_df = target_df.copy()

    for index, row in filter_df.iterrows():
        id_prod = row["IdProd"]

        if id_prod not in REGRAS_CLASSIFICACAO_PARCIAL:
            continue

        if row["NIVEL_3"] != VALOR_NAO_CLASSIFICADO:
            continue

        coluna_busca = REGRAS_CLASSIFICACAO_PARCIAL[id_prod]
        search_str = str(row[coluna_busca])

        # >>> REVISAR: normalização aplicada somente a estes casos.
        from .normalizacao import normalizar_texto
        search_str = normalizar_texto(search_str)

        if search_str in CORRECOES_CLASSIFICACAO:
            target_df.loc[index, "NIVEL_3"] = (
                CORRECOES_CLASSIFICACAO[search_str]
            )
        else:
            target_df.loc[index, "NIVEL_3"] = buscar_valor(
                rbc_nao_unicas["N3"],
                "NIVEL_3",
                search_str,
            )

            target_df.loc[index, "NIVEL_4"] = buscar_valor(
                rbc_nao_unicas["N4"],
                "NIVEL_4",
                search_str,
            )

        target_df.loc[
            index,
            "Result",
        ] = RESULTADO_PARCIAL_RESOLVIDA

    return target_df
