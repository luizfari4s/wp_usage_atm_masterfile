from __future__ import annotations

from pathlib import Path
from regras import aplicar_regra


from .charge import carregar_bases
from .normalizacao import preparar_masterfile
from .regras import (
    separar_rbc_por_unicidade,
    ids_nao_classificaveis,
    aplicar_rbc,
    juntar_niveis,
    classificar_produtos_novos,
    resolver_classificacao_parcial,
)

def rbc_level(mf_atual_normalizado,level_data,rule_table):
    
    mf_atual_normalizado['DescUsage'] = mf_atual_normalizado.apply(
        lambda r: aplicar_regra(r['IdProd'], rule_table, r),
        axis=1
        )

    mf_atual_normalizado['DescUsage'] = mf_atual_normalizado['DescUsage'].str.replace('\u00A0', ' ', regex=False)

    merged = mf_atual_normalizado.merge(level_data, on='IdArtigo', how= 'left')
    merged = merged.dropna(axis=1, how="all")

    return merged


def finalizar(old_products, new_products):
    import pandas as pd

    dados_finais = pd.concat(
        [old_products, new_products],
        ignore_index=True,
    )

    dados_finais["DescUsage"] = (
        dados_finais["DescUsage"]
        .str.title()
    )

    for coluna in [
        "NIVEL_1",
        "NIVEL_2",
        "NIVEL_3",
        "NIVEL_4",
    ]:
        dados_finais[coluna] = dados_finais[coluna].replace(
            "o",
            "",
        )

    return dados_finais


def exportar(df, caminho_saida):
    caminho_saida = Path(caminho_saida)
    caminho_saida.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        caminho_saida,
        index=False,
        encoding="latin1",
        sep=";",
    )
