from __future__ import annotations

from .config import ENCODING, SEPARATOR
from pandas import read_csv

from config import input_projeto, rbc_data

def carregamento():
    from pandas import read_csv
    

    # carregamento drbc base
    rule_table = read_csv(f'{rbc_data}/rule_table_with_rulemap_v2.csv', sep = ';',encoding='latin1')
    level_data = read_csv(f'{rbc_data}/level_data.csv', sep = ';',encoding='latin1')

    # carregamento de rbc por nível
    rbc_n1 = read_csv(f'{rbc_data}/RBC_N1.csv', sep = ';',encoding='latin1')
    rbc_n2 = read_csv(f'{rbc_data}/RBC_N2.csv', sep = ';',encoding='latin1')
    rbc_n3 = read_csv(f'{rbc_data}/RBC_N3.csv', sep = ';',encoding='latin1')
    rbc_n4 = read_csv(f'{rbc_data}/RBC_N4.csv', sep = ';',encoding='latin1')

    # carregamento do mf_atual

    mf_atual = read_csv(f'{input_projeto}/MF_Atual.csv')

    return mf_atual, rule_table, level_data, rbc_n1, rbc_n2, rbc_n3, rbc_n4
 