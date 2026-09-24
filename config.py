"""
Configurações e regras que estavam hardcoded no notebook.

>>> REVISAR AQUI
Este arquivo é o primeiro lugar para revisar quando uma regra de negócio mudar.
A ideia é manter o pipeline estável e concentrar as exceções/configurações.
"""
from configparser import ConfigParser
from pathlib import Path
config = ConfigParser()

config.read(
        Path.home() / "Documents" / "wp_central_atm" / "config.ini",
        encoding="utf-8"
)

dl = Path.home() / config["datalake"]["caminho"]

datalake = str(dl)
input_projeto = f'{datalake}/do_mf_usage/input'
output_projeto = f'{datalake}/do_mf_usage/output'
rbc_data = f'{datalake}/do_mf_usage/rbc'

ENCODING = "latin1"
SEPARATOR = ";"

COLUNAS_DESCARTAR = {
    "CdC06", "Clas06",
    "CdC07", "Clas07",
    "CdC08", "Clas08",
    "CdC09", "Clas09",
}

# >>> REVISAR: estas substituições são regras de normalização de negócio.
NORMALIZACOES_EXATAS = {
    "Agua Embalada": "Agua Mineral",
    "Snacks": "Salgadinho",
}

# >>> REVISAR: valores considerados como ausência de informação.
VALORES_AUSENTES = {
    "Clas01": ["NAO INFORMADO"],
    "Clas02": ["NAO INFORMADO"],
    "Clas03": ["NAO INFORMADO"],
    "Clas04": ["NAO INFORMADO"],
    "Clas05": ["NAO INFORMADO"],
    "Marca": ["NAO REQUERIDO", "NAO INFORMADO", "Sem Marca"],
    "Fabricante": ["NAO REQUERIDO", "NAO INFORMADO"],
    "Sub": ["Codebook VS"],
}

# >>> REVISAR: filtro de Sub usado para retirar registros do processamento.
SUB_EXCLUIDOS = {
    "Codebook OOH",
    "Codebook OOH Barra / Tablete / Candy Bar",
    "Codebook OOH Batata Frita Na Hora",
    "Codebook OOH Bolos Industrializados",
    "Codebook OOH Bombom",
    "Codebook OOH Bombom Individual / Trufa",
    "Codebook OOH Caixa de Chocolate / Pacote de Choco",
    "Codebook OOH Casquinha",
    "Codebook OOH Chopeira",
    "Codebook OOH Com Gas",
    "Codebook OOH Copo / Pote",
    "Codebook OOH De Beber",
    "Codebook OOH De Colher",
    "Codebook OOH Doce",
    "Codebook OOH Docinhos e Tortas",
    "Codebook OOH Lata / Garrafa",
    "Codebook OOH Líquido",
    "Codebook OOH Nao Informado",
    "Codebook OOH Outros Formatos",
    "Codebook OOH Picolé",
    "Codebook OOH Pipoca Pronta",
    "Codebook OOH Salgadinhos Industrializados",
    "Codebook OOH Salgado",
    "Codebook OOH Salgados preparado na hora",
    "Codebook OOH Sem Gas",
    "Codebook OOH Suco de Frutas Feito na Hora",
    "Codebook OOH Suco de Frutas Industrializado",
}

ATIVOS_EXCLUIDOS = {"AR"}

# >>> REVISAR: exceções individuais de classificação parcial.
# Formato: IdProd -> coluna da base usada para localizar N3/N4.
REGRAS_CLASSIFICACAO_PARCIAL = {
    200: "Clas01",
    63: "Clas02",
    686: "Sub",
    201: "Sub",
    58: "Sub",
    287: "Producto",
    212: "Sub",
    622: "Sub",
    269: "Clas02",
}

# >>> REVISAR: correções manuais de inconsistências conhecidas.
CORRECOES_CLASSIFICACAO = {
    "MISTA (VEGETAL + MANTEIGA)": "MARGARINA + MANTEIGA / MISTA",
    "DOCINHOS / RECHEIOS / COBERTOS": "LEITE CONDENSADO",
    "FIAMBRE / AFIAMBRADO / LANCHE": "FIAMBRE / AFIAMBRADO",
}

# Valor usado no notebook para representar classificação não encontrada.
VALOR_NAO_CLASSIFICADO = "o"

RESULTADO_RBC = "Classificado Com RBC"
RESULTADO_HISTORICO = "Classificado Com Histórico"
RESULTADO_PARCIAL = "Classificação Parcial"
RESULTADO_CONFLITO = "Conflito"
RESULTADO_PARCIAL_RESOLVIDA = "Classificação Parcial Resolvida"
