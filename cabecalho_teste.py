import pandas as pd

def gerar_cabecalho_bpa(arquivo_entrada, arquivo_saida):
    # carregar dados do arquivo CSV
    df = pd.read_csv(arquivo_entrada)
    
    # lista para armazenar as linhas formatadas

    linhas_formatadas = []
    
  # passar por cada linha da tabela de dados
    for _, linha in df.iterrows():

        linha_formatada = (
            f"{linha['cbc-hdr']:02}"  # indicador de linha do Header (2 dígitos)
            f"#{linha['cbc-hdr-indicador']}"  # indicador do cabeçalho (#BPA#)
            f"{linha['cbc-mvm']:<6}"  # ano e mês de processamento (AAAAMM)
            f"{str(linha['cbc-lin']).zfill(6)}"  # número de linhas com zeros à esquerda
            f"{str(linha['cbc-flh']).zfill(6)}"  # quantidade de folhas com zeros à esquerda
            f"{linha['cbc-smt-vrf']:<4}"  # campo de controle (1111 a 2221)
            f"{linha['cbc-rsp']:<30}"  # nome do órgão de origem
            f"{linha['cbc-sgl']:<6}"  # sigla do órgão de origem
            f"{str(linha['cbc-cgccpf']).zfill(14)}"  # CGC/CPF com zeros à esquerda
            f"{linha['cbc-dst']:<40}"  # nome do órgão de saúde destino
            f"{linha['cbc-dst-in']:1}"  # indicador do órgão destino (E ou M)
            f"{linha['cbc_versao']:<10}"  # versão do sistema
        )
        # adicionar linha ao resultado
        linhas_formatadas.append(linha_formatada)
    
    # salvar as linhas no arquivo de saída
    with open(arquivo_saida, 'w') as arquivo:
        arquivo.write("\n".join(linhas_formatadas))
    print(f"Cabeçalhos formatados salvos em {arquivo_saida}")

# Exemplo de uso
gerar_cabecalho_bpa("arquivo_entrada.csv", "saida.txt")
