import pandas as pd
from app.utils.bpa_validator import BPAValidator

class BPAGenerator:
    # Constantes do arquivo BPA
    HEADER_TYPE = "01"
    BPA_C_TYPE = "02"
    BPA_I_TYPE = "03"
    ORIGEM = "EXT"

    def __init__(self):
        self.validator = BPAValidator()

    def generate_header(self, header_data: dict) -> str:
        """Gera linha de cabeçalho do arquivo BPA"""
        if not self.validator.validate_header(header_data):
            raise ValueError(f"Dados do cabeçalho inválidos: {', '.join(self.validator.get_errors())}")

        total_lines = str(header_data.get('total_lines', 1)).zfill(6)
        total_sheets = str(header_data.get('total_sheets', 1)).zfill(6)
        control_field = "1111"
        
        year_month = str(header_data['year_month']).zfill(6)
        org_name = str(header_data['org_name']).ljust(30)
        org_acronym = str(header_data.get('org_acronym', '')).ljust(6)
        cgc_cpf = str(header_data['cgc_cpf']).zfill(14)
        dest_name = str(header_data['dest_name']).ljust(40)
        dest_type = header_data['dest_type']
        version = str(header_data.get('version', '1.0.0')).ljust(10)
        
        return (f"{self.HEADER_TYPE}#BPA#{year_month}{total_lines}{total_sheets}{control_field}"
                f"{org_name}{org_acronym}{cgc_cpf}{dest_name}{dest_type}{version}\r\n")

    def generate_bpa_c(self, row: pd.Series) -> str:
        """Gera linha de BPA Consolidado"""
        if not self.validator.validate_bpa_c(row):
            raise ValueError(f"Dados do BPA Consolidado inválidos: {', '.join(self.validator.get_errors())}")
        
        line = self.BPA_C_TYPE
        line += str(row['cnes']).zfill(self.validator.REQUIRED_SIZES['cnes'])
        line += str(row['competencia']).zfill(self.validator.REQUIRED_SIZES['competencia'])
        line += str(row['cbo']).ljust(self.validator.REQUIRED_SIZES['cbo'])
        line += str(row['folha']).zfill(3)
        line += str(row['sequencial']).zfill(2)
        line += str(row['procedimento']).zfill(self.validator.REQUIRED_SIZES['procedimento'])
        line += str(row['idade']).zfill(self.validator.REQUIRED_SIZES['idade'])
        line += str(row['quantidade']).zfill(6)
        line += self.ORIGEM
        line += "\r\n"
        
        return line

    def generate_bpa_i(self, row: pd.Series) -> str:
        """Gera linha de BPA Individualizado"""
        if not self.validator.validate_bpa_i(row):
            raise ValueError(f"Dados do BPA Individualizado inválidos: {', '.join(self.validator.get_errors())}")
                             
        line = self.BPA_I_TYPE
        line += str(row['cnes']).zfill(self.validator.REQUIRED_SIZES['cnes'])
        line += str(row['competencia']).zfill(self.validator.REQUIRED_SIZES['competencia'])
        line += str(row['cns_profissional']).zfill(self.validator.REQUIRED_SIZES['cns'])
        line += str(row['cbo']).ljust(self.validator.REQUIRED_SIZES['cbo'])
        
        data_atend = pd.to_datetime(row['data_atendimento']).strftime('%Y%m%d')
        line += data_atend
        
        line += str(row['folha']).zfill(3)
        line += str(row['sequencial']).zfill(2)
        line += str(row['procedimento']).zfill(self.validator.REQUIRED_SIZES['procedimento'])
        line += str(row['cns_paciente']).zfill(self.validator.REQUIRED_SIZES['cns'])
        line += str(row['sexo']).upper()
        line += str(row['codigo_municipio']).zfill(6)
        line += str(row['cid']).ljust(4)
        line += str(row['idade']).zfill(self.validator.REQUIRED_SIZES['idade'])
        line += str(row['quantidade']).zfill(6)
        line += str(row.get('carater_atendimento', '01')).zfill(2)
        line += str(row.get('numero_autorizacao', '')).ljust(13)
        line += self.ORIGEM
        line += str(row['nome_paciente']).ljust(30)
        
        dt_nasc = pd.to_datetime(row['data_nascimento']).strftime('%Y%m%d')
        line += dt_nasc
        
        line += str(row.get('raca', '01')).zfill(2)
        line += str(row.get('etnia', '')).ljust(4)
        line += str(row.get('nacionalidade', '010')).zfill(3)
        line += str(row.get('servico', '')).ljust(3)
        line += str(row.get('classificacao', '')).ljust(3)
        line += str(row.get('equipe_seq', '')).ljust(8)
        line += str(row.get('equipe_area', '')).ljust(4)
        line += str(row.get('cnpj', '')).ljust(14)
        line += str(row.get('cep', '')).ljust(8)
        line += str(row.get('codigo_logradouro', '')).ljust(3)
        line += str(row.get('endereco', '')).ljust(30)
        line += str(row.get('complemento', '')).ljust(10)
        line += str(row.get('numero', '')).ljust(5)
        line += str(row.get('bairro', '')).ljust(30)
        line += str(row.get('telefone', '')).ljust(11)
        line += str(row.get('email', '')).ljust(40)
        line += str(row.get('ine', '')).ljust(10)
        line += "\r\n"
        
        return line
    