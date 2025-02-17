import pandas as pd
from app.utils.bpa_validator import BPAValidator
from app.utils.bpa_formatter import BPAFormatter

class BPAGenerator:
    # Constantes do arquivo BPA
    HEADER_TYPE = "01"
    BPA_C_TYPE = "02"
    BPA_I_TYPE = "03"
    ORIGEM = "EXT"
    MAX_LINHAS_POR_FOLHA = 90

    def __init__(self):
        self.validator = BPAValidator()
        self.folha_atual = 1
        self.linhas_na_folha = 0

    def atualizar_folha(self):
        """Verifica e atualiza a contagem de folhas conforme o limite de linhas."""
        if self.linhas_na_folha >= self.MAX_LINHAS_POR_FOLHA:
            self.folha_atual += 1
            self.linhas_na_folha = 0

    def generate_header(self, header_data: dict) -> str:
        # Verifica se a chave 'year_month' existe, senão tenta usar 'competencia'
        year_month = header_data.get("year_month") or header_data.get("competencia")
        
        if not year_month:
            raise ValueError("❌ Campo obrigatório ausente: year_month (ou competencia)")

        total_lines = str(header_data.get('total_lines', 1)).zfill(6)
        total_sheets = str(header_data.get('total_sheets', 1)).zfill(6)
        control_field = "1111"
        
        return (f"{self.HEADER_TYPE}#BPA#{year_month.zfill(6)}"
                f"{total_lines}{total_sheets}{control_field}"
                f"{header_data['org_name'].ljust(30)}"
                f"{header_data.get('org_acronym', '').ljust(6)}"
                f"{header_data['cgc_cpf'].zfill(14)}"
                f"{header_data['dest_name'].ljust(40)}"
                f"{header_data['dest_type']}"
                f"{header_data.get('version', '1.0.0').ljust(10)}\r\n")

    def generate_bpa_c(self, row: pd.Series) -> str:
        """Gera linha de BPA Consolidado"""
        row_dict = BPAFormatter.format_data(row.to_dict())

        if not self.validator.validate_bpa_c(row_dict):
            raise ValueError(f"Dados do BPA Consolidado inválidos: {', '.join(self.validator.get_errors())}")
        
        self.atualizar_folha()
        self.linhas_na_folha += 1
        
        return (f"{self.BPA_C_TYPE}{row_dict['cnes']}{row_dict['competencia']}"
                f"{row_dict['cbo']}{str(self.folha_atual).zfill(3)}{row_dict['sequencial']}"
                f"{row_dict['procedimento']}{row_dict['idade']}{row_dict['quantidade']}"
                f"{self.ORIGEM}\r\n")

    def generate_bpa_i(self, row: pd.Series) -> str:
        """Gera linha de BPA Individualizado"""
        row_dict = BPAFormatter.format_data(row.to_dict())

        if not self.validator.validate_bpa_i(row_dict):
            raise ValueError(f"Dados do BPA Individualizado inválidos: {', '.join(self.validator.get_errors())}")
                              
        self.atualizar_folha()
        self.linhas_na_folha += 1

        return (f"{self.BPA_I_TYPE}{row_dict['cnes']}{row_dict['competencia']}"
                f"{row_dict['cns_profissional']}{row_dict['cbo']}{row_dict['data_atendimento']}"
                f"{str(self.folha_atual).zfill(3)}{row_dict['sequencial']}"
                f"{row_dict['procedimento']}{row_dict['cns_paciente']}{row_dict['sexo']}"
                f"{row_dict['codigo_municipio']}{row_dict['cid']}{row_dict['idade']}"
                f"{row_dict['quantidade']}{row_dict['carater_atendimento']}"
                f"{row_dict['numero_autorizacao']}{self.ORIGEM}{row_dict['nome_paciente']}"
                f"{row_dict['data_nascimento']}{row_dict['raca']}{row_dict['etnia']}"
                f"{row_dict['nacionalidade']}{row_dict['servico']}{row_dict['classificacao']}"
                f"{row_dict['equipe_seq']}{row_dict['equipe_area']}{row_dict['cnpj']}"
                f"{row_dict['cep']}{row_dict['codigo_logradouro']}{row_dict['endereco']}"
                f"{row_dict['complemento']}{row_dict['numero']}{row_dict['bairro']}"
                f"{row_dict['telefone']}{row_dict['email']}{row_dict['ine']}\r\n")
