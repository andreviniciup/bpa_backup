import pandas as pd

def gerar_cabecalho_bpa(arquivo_entrada, arquivo_saida):
    """
    Gera o cabeçalho BPA formatado como uma única linha, sem espaços extras entre os campos.
    """
    # Carregar dados do arquivo CSV
    df = pd.read_csv(arquivo_entrada)
    
    # Lista para armazenar as linhas formatadas
    linhas_formatadas = []
    
    # Passar por cada linha da tabela de dados
    for _, linha in df.iterrows():
        linha_formatada = (
            f"{int(linha['cbc-hdr']):02}"  # Indicador de linha do Header (2 dígitos)
            + f"#{linha['cbc-hdr-indicador']}"  # Indicador do cabeçalho (#BPA#)
            + f"{str(linha['cbc-mvm']).zfill(6)}"  # Ano e mês de processamento (AAAAMM)
            + f"{str(linha['cbc-lin']).zfill(6)}"  # Número de linhas (zeros à esquerda)
            + f"{str(linha['cbc-flh']).zfill(6)}"  # Quantidade de folhas (zeros à esquerda)
            + f"{str(linha['cbc-smt-vrf']):<4}".strip()  # Campo de controle (1111 a 2221), removendo espaços
            + f"{linha['cbc-rsp'].replace(' ', '')}"  # Nome do órgão de origem (remover espaços internos)
            + f"{linha['cbc-sgl'].replace(' ', '')}"  # Sigla do órgão de origem (remover espaços internos)
            + f"{str(linha['cbc-cgccpf']).zfill(14)}"  # CGC/CPF (zeros à esquerda)
            + f"{linha['cbc-dst'].replace(' ', ''):<40}".rstrip()  # Nome do órgão de saúde destino (remover espaços internos)
            + f"{linha['cbc-dst-in']:1}"  # Indicador do órgão destino (E ou M)
            + f"{linha['cbc_versao']}"  # Versão do sistema
        )
        
        # Adicionar linha ao resultado
        linhas_formatadas.append(linha_formatada)
    
    # Salvar as linhas no arquivo de saída
    with open(arquivo_saida, 'w', encoding='utf-8') as arquivo:
        arquivo.write("\n".join(linhas_formatadas))
    
    print(f"Cabeçalhos formatados salvos em {arquivo_saida}")

# Exemplo de uso
gerar_cabecalho_bpa("arquivo_entrada.csv", "saida.txt")
