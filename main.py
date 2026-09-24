from config import input_projeto,output_projeto, rbc_data
from charge import carregamento 
from normalizacao import normalizacao
from pipeline import rbc_level

def main():
    
    mf_atual, rule_table, level_data, rbc_n1, rbc_n2, rbc_n3, rbc_n4 = carregamento()
    mf_atual_normalizado = normalizacao(mf_atual)

    merged = rbc_level(mf_atual_normalizado, level_data, rule_table)

    
    