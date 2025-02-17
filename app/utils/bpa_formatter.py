import pandas as pd

class BPAFormatter:
    #classe responsavel por formatar os dados para o bpa

    def format_cnes(value: str) -> str:
        return str(value).zfill(7)

    def format_competencia(value: str) -> str:
        return str(value).zfill(6)

    def format_cns(value: str) -> str:
        return str(value).zfill(15)

    def format_cbo(value: str) -> str:
        return str(value).ljust(6)

    def format_data(value: str) -> str:
        return pd.to_datetime(value).strftime('%Y%m%d')

    def format_folha(value: str) -> str:
        return str(value).zfill(3)

    def format_sequencial(value: str) -> str:
        return str(value).zfill(2)

    def format_procedimento(value: str) -> str:
        return str(value).zfill(10)

    def format_codigo_municipio(value: str) -> str:
        return str(value).zfill(6)

    def format_cid(value: str) -> str:
        return str(value).ljust(4)

    def format_idade(value: str) -> str:
        return str(value).zfill(3)

    def format_quantidade(value: str) -> str:
        return str(value).zfill(6)

    def format_carater_atendimento(value: str) -> str:
        return str(value).zfill(2)

    def format_numero_autorizacao(value: str) -> str:
        return str(value).ljust(13)

    def format_nome_paciente(value: str) -> str:
        return str(value).ljust(30)

    def format_raca(value: str) -> str:
        return str(value).zfill(2)

    def format_etnia(value: str) -> str:
        return str(value).ljust(4)

    def format_nacionalidade(value: str) -> str:
        return str(value).zfill(3)

    def format_servico(value: str) -> str:
        return str(value).ljust(3)

    def format_classificacao(value: str) -> str:
        return str(value).ljust(3)

    def format_equipe_seq(value: str) -> str:
        return str(value).ljust(8)

    def format_equipe_area(value: str) -> str:
        return str(value).ljust(4)

    def format_cnpj(value: str) -> str:
        return str(value).ljust(14)

    def format_cep(value: str) -> str:
        return str(value).ljust(8)

    def format_codigo_logradouro(value: str) -> str:
        return str(value).ljust(3)

    def format_endereco(value: str) -> str:
        return str(value).ljust(30)

    def format_complemento(value: str) -> str:
        return str(value).ljust(10)

    def format_numero(value: str) -> str:
        return str(value).ljust(5)

    def format_bairro(value: str) -> str:
        return str(value).ljust(30)

    def format_telefone(value: str) -> str:
        return str(value).ljust(11)

    def format_email(value: str) -> str:
        return str(value).ljust(40)

    def format_ine(value: str) -> str:
        return str(value).ljust(10)

    def format_data_nascimento(value: str) -> str:
        return pd.to_datetime(value).strftime('%Y%m%d')


    def format_data(cls, row: dict) -> dict:
        return {key: getattr(cls, f'format_{key}')(value) if hasattr(cls, f'format_{key}') else value for key, value in row.items()}
