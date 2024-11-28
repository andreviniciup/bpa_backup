import pandas as pd

class BPAGenerator:
    def __init__(self):
        self.HEADER_TYPE = "01"
        self.BPA_C_TYPE = "02"
        self.BPA_I_TYPE = "03"

    def generate_header(self, header_data: dict) -> str:
        """Gera linha de cabeçalho do arquivo BPA"""
        total_lines = str(header_data.get('total_lines', 1)).zfill(6)
        total_sheets = str(header_data.get('total_sheets', 1)).zfill(6)
        control_field = "1111"
        
        year_month = str(header_data['year_month']).ljust(6)
        org_name = str(header_data['org_name']).ljust(30)
        org_acronym = str(header_data['org_acronym']).ljust(6)
        cgc_cpf = str(header_data['cgc_cpf']).zfill(14)
        dest_name = str(header_data['dest_name']).ljust(40)
        dest_type = header_data['dest_type']
        version = str(header_data.get('version', '1.0.0')).ljust(10)
        
        header = (f"{self.HEADER_TYPE}#BPA#{year_month}{total_lines}{total_sheets}{control_field}"
                 f"{org_name}{org_acronym}{cgc_cpf}{dest_name}{dest_type}{version}\r\n")
        
        return header

    def generate_bpa_c(self, row: pd.Series) -> str:
        """Gera linha de BPA Consolidado"""
        line = self.BPA_C_TYPE
        line += str(row['cnes']).zfill(7)
        line += str(row['competencia']).zfill(6)
        line += str(row['cbo']).ljust(6)
        line += str(row['folha']).zfill(3)
        line += str(row['sequencial']).zfill(2)
        line += str(row['procedimento']).zfill(10)
        line += str(row['idade']).zfill(3)
        line += str(row['quantidade']).zfill(6)
        line += "EXT"
        line += "\r\n"
        
        return line

    def generate_bpa_i(self, row: pd.Series) -> str:
        """Gera linha de BPA Individualizado"""
        line = self.BPA_I_TYPE
        
        line += str(row['cnes']).zfill(7)
        line += str(row['competencia']).zfill(6)
        line += str(row['cns_profissional']).zfill(15)
        line += str(row['cbo']).ljust(6)
        
        data_atend = pd.to_datetime(row['data_atendimento']).strftime('%Y%m%d')
        line += data_atend
        
        line += str(row['folha']).zfill(3)
        line += str(row['sequencial']).zfill(2)
        line += str(row['procedimento']).zfill(10)
        line += str(row['cns_paciente']).zfill(15)
        line += str(row['sexo']).upper()
        line += str(row['codigo_municipio']).zfill(6)
        line += str(row['cid']).ljust(4)
        line += str(row['idade']).zfill(3)
        line += str(row['quantidade']).zfill(6)
        line += str(row.get('carater_atendimento', '01')).zfill(2)
        line += str(row.get('numero_autorizacao', '')).ljust(13)
        line += "EXT"  # Origem fixo
        line += str(row['nome_paciente']).ljust(30)
        
        dt_nasc = pd.to_datetime(row['data_nascimento']).strftime('%Y%m%d')
        line += dt_nasc
        
        line += str(row.get('raca', '01')).zfill(2)
        line += str(row.get('etnia', '')).ljust(4)
        line += str(row.get('nacionalidade', '010')).zfill(3)
        
        service = str(row.get('servico', '')).ljust(3)
        classification = str(row.get('classificacao', '')).ljust(3)
        team_seq = str(row.get('equipe_seq', '')).ljust(8)
        team_area = str(row.get('equipe_area', '')).ljust(4)
        cnpj = str(row.get('cnpj', '')).ljust(14)
        cep = str(row.get('cep', '')).ljust(8)
        address_code = str(row.get('codigo_logradouro', '')).ljust(3)
        address = str(row.get('endereco', '')).ljust(30)
        complement = str(row.get('complemento', '')).ljust(10)
        number = str(row.get('numero', '')).ljust(5)
        neighborhood = str(row.get('bairro', '')).ljust(30)
        phone = str(row.get('telefone', '')).ljust(11)
        email = str(row.get('email', '')).ljust(40)
        ine = str(row.get('ine', '')).ljust(10)
        
        line += f"{service}{classification}{team_seq}{team_area}{cnpj}{cep}"
        line += f"{address_code}{address}{complement}{number}{neighborhood}"
        line += f"{phone}{email}{ine}\r\n"
        
        return line
