from __future__ import annotations

import unicodedata
import pandas as pd

from config import (
    COLUNAS_DESCARTAR,
    NORMALIZACOES_EXATAS,
    VALORES_AUSENTES,
    SUB_EXCLUIDOS,
    ATIVOS_EXCLUIDOS,
)


def normalizacao(mf_atual):
    # 1º etapa
    aux = mf_atual.copy()

    aux['DescUsage'] = None

    #
    to_drop = {'CdC06','Clas06',
            'CdC07','Clas07',
            'CdC08','Clas08',
            'CdC09','Clas09'}

    aux.drop(columns= to_drop, inplace=True)

    # 2º etapa
    aux.Clas01 = aux.Clas01.str.replace('NAO INFORMADO', '')
    aux.Clas02 = aux.Clas02.str.replace('NAO INFORMADO', '')
    aux.Clas03 = aux.Clas03.str.replace('NAO INFORMADO', '')
    aux.Clas04 = aux.Clas04.str.replace('NAO INFORMADO', '')
    aux.Clas05 = aux.Clas05.str.replace('NAO INFORMADO', '')

    aux.Marca = aux.Marca.str.replace('NAO REQUERIDO', '')
    aux.Marca = aux.Marca.str.replace('NAO INFORMADO', '')
    aux.Marca = aux.Marca.str.replace('Sem Marca', '')


    aux.Fabricante = aux.Fabricante.str.replace('NAO REQUERIDO', '')
    aux.Fabricante = aux.Fabricante.str.replace('NAO INFORMADO', '')

    aux.Sub = aux.Sub.str.replace('Codebook VS', '')
    aux.Producto = aux.Producto.str.replace('Agua Embalada', 'Agua Mineral')
    aux.Producto = aux.Producto.str.replace('Snacks', 'Salgadinho')

    # marcação da coluna de movimento de STR para Mililitros
    aux.loc[
        aux.Contenido.str.contains('ML'),
        "Contenido"
    ] = aux["Contenido"] + " STR_CHANGE_ML"

    # marcação da coluna de movimento de STR para Gramas
    aux.loc[
        aux.Contenido.str.contains('GR'),
        "Contenido"
    ] = aux["Contenido"] + " STR_CHANGE_GR"

    aux.Contenido = aux.Contenido.str.replace('ML ', '')
    aux.Contenido = aux.Contenido.str.replace('GR ', '')

    aux.Contenido = aux.Contenido.str.replace('STR_CHANGE_ML', 'ml')
    aux.Contenido = aux.Contenido.str.replace('STR_CHANGE_GR', 'gr')


    aux.drop(columns={'Creado','Fuente'},inplace=True)

    aux = aux.loc[~(aux.Sub.isin(SUB_EXCLUIDOS)) & ~(aux.Activo == ('AR'))]

    





