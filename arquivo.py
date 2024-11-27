import pandas as pd

# Criar um DataFrame com dados de exemplo
dados = {
    "cbc-hdr": [1, 2],
    "cbc-hdr-indicador": ["BPA#", "BPA#"],
    "cbc-mvm": [202106, 202107],
    "cbc-lin": [97, 85],
    "cbc-flh": [5, 6],
    "cbc-smt-vrf": [1291, 1111],
    "cbc-rsp": ["Secretaria de Saúde", "Unidade Básica de Saúde"],
    "cbc-sgl": ["SMS", "UBS"],
    "cbc-cgccpf": [12345678901234, 98765432109876],
    "cbc-dst": ["Hospital Municipal", "Posto Regional"],
    "cbc-dst-in": ["E", "M"],
    "cbc_versao": ["1.0", "2.0"]
}

# Converter para DataFrame
df = pd.DataFrame(dados)

# Salvar em arquivo CSV
df.to_csv("arquivo_entrada.csv", index=False)
print("Arquivo 'arquivo_entrada.csv' criado com sucesso!")
