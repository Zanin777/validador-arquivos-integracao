import re
import json
import os

def validar_cnpj(cnpj: str) -> bool:

    cnpj = re.sub(r'\D', '', cnpj)
      
    if len(cnpj) != 14 or len(set(cnpj)) == 1:
        return False

    def calcular_digito(cnpj_parcial: str, pesos: list) -> int:
        soma = sum(int(digito) * peso for digito, peso in zip(cnpj_parcial, pesos))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    pesos_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    digito_1 = calcular_digito(cnpj[:12], pesos_1)

    pesos_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    digito_2 = calcular_digito(cnpj[:12] + str(digito_1), pesos_2)
    
    return cnpj[-2:] == f"{digito_1}{digito_2}"

def analisar_arquivo_integracao(caminho_txt: str, caminho_json: str):
  
    relatorio_erros = []

    try:
        
        with open(caminho_txt, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()
        if not linhas:
            print("Aviso: O arquivo está vazio.")
            return
        for num_linha, linha in enumerate(linhas, start=1):
            linha = linha.rstrip('\n\r')
            try:
                if not linha.strip():
                    continue  
                tipo_registro = linha[0]
                if tipo_registro == '0':
                    if len(linha) < 45:
                        raise ValueError(f"Header incompleto. Esperado 45 caracteres, obtido {len(linha)}.")
                    cnpj_extraido = linha[1:15]
                    if not re.match(r'^\d{14}$', cnpj_extraido):
                        raise ValueError(f"CNPJ '{cnpj_extraido}' contém caracteres não numéricos.")  
                    if not validar_cnpj(cnpj_extraido):
                        raise ValueError(f"O CNPJ '{cnpj_extraido}' foi rejeitado na validação matemática do dígito verificador.")

                elif tipo_registro == '1':
                    if len(linha) < 29:
                        raise ValueError(f"Linha de detalhe incompleta. Esperado 29 caracteres, obtido {len(linha)}.")
                    valor = linha[11:21].strip()
                    data_pagamento = linha[21:29]

                    if not re.match(r'^\d+$', valor):
                        raise ValueError(f"O campo 'Valor' ({valor}) deve conter apenas números.")
                    if not re.match(r'^(0[1-9]|[12][0-9]|3[01])(0[1-9]|1[0-2])\d{4}$', data_pagamento):
                        raise ValueError(f"Data '{data_pagamento}' inválida. Use o formato DDMMAAAA.")
                
                elif tipo_registro == '9':
                    pass 
                else:
                    raise ValueError(f"Tipo de registro '{tipo_registro}' é desconhecido. Permitidos: 0, 1, 9.")

            except ValueError as erro_validacao:
                relatorio_erros.append({
                    "linha": num_linha,
                    "tipo_registro": tipo_registro if 'tipo_registro' in locals() else "Desconhecido",
                    "conteudo_suspeito": linha[:30] + ("..." if len(linha) > 30 else ""),
                    "motivo_rejeicao": str(erro_validacao)
                })
                

    except FileNotFoundError:
        print(f"Erro Fatal: O arquivo '{caminho_txt}' não foi encontrado.")
        return
    except Exception as e:
        print(f"Erro inesperado ao processar o arquivo: {e}")
        return
    with open(caminho_json, 'w', encoding='utf-8') as arquivo_json:
        json.dump(relatorio_erros, arquivo_json, indent=4, ensure_ascii=False)

    print(f"Validação concluída. {len(relatorio_erros)} erro(s) encontrado(s).")
    print(f"Relatório gerado em: {caminho_json}")
if __name__ == "__main__":
    analisar_arquivo_integracao('remessa_teste.txt', 'relatorio_erros.json')
