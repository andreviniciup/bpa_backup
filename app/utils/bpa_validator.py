import pandas as pd
from datetime import datetime

class BPAValidator:
    # Constantes para tamanhos dos campos
    REQUIRED_SIZES = {
        'cns': 15,
        'cnes': 7,
        'procedimento': 10,
        'cbo': 6,
        'idade': 3,
        'competencia': 6
    }
    
    # Constantes para valores válidos
    MAX_AGE = 130
    MIN_AGE = 0
    VALID_DEST_TYPES = ['M', 'E']
    VALID_SEX = ['M', 'F']

    # Campos obrigatórios por tipo de registro
    REQUIRED_HEADER_FIELDS = ['year_month', 'org_name', 'cgc_cpf', 'dest_name', 'dest_type']
    REQUIRED_BPA_C_FIELDS = ['cnes', 'competencia', 'cbo', 'folha', 'sequencial', 'procedimento', 'quantidade']
    REQUIRED_BPA_I_FIELDS = ['cnes', 'competencia', 'cns_profissional', 'cbo', 'data_atendimento', 'folha', 
                            'sequencial', 'procedimento', 'cns_paciente', 'sexo', 'codigo_municipio', 'nome_paciente']

    def __init__(self):
        self.errors = []

    def _validate_digits(self, value: str, field_name: str, size: int) -> bool:
        """Valida se um campo contém apenas dígitos e tem o tamanho correto"""
        if not value:
            self.errors.append(f"{field_name} não pode estar vazio")
            return False
        
        value_str = str(value).strip()
        if not value_str.isdigit():
            self.errors.append(f"{field_name} deve conter apenas números")
            return False
            
        if len(value_str) != size:
            self.errors.append(f"{field_name} deve ter {size} dígitos")
            return False
            
        return True

    def _validate_date(self, date_str: str, field_name: str) -> bool:
        """Valida formato de data YYYY-MM-DD"""
        try:
            if isinstance(date_str, str):
                datetime.strptime(date_str, '%Y-%m-%d')
                return True
        except ValueError:
            self.errors.append(f"{field_name} deve estar no formato YYYY-MM-DD")
            return False
        return True

    def validate_cns(self, cns: str) -> bool:
        """Valida dígito verificador do CNS"""
        if not self._validate_digits(cns, "CNS", self.REQUIRED_SIZES['cns']):
            return False
        
        # Implementação do algoritmo de validação do CNS
        if str(cns).startswith(('1', '2')):  # CNS Definitivo
            pis = str(cns)[:-2]
            dv = str(cns)[-2:]

            soma = 0
            for i in range(11):
                soma += int(pis[i]) * (15 - i)
            
            resto = soma % 11
            dv1 = 11 - resto
            
            if dv1 == 11:
                dv1 = 0
            if dv1 == 10:
                soma = 0
                for i in range(11):
                    soma += int(pis[i]) * (15 - i)
                soma += dv1 * 2
                resto = soma % 11
                dv1 = 11 - resto
                    
            dv_calculado = str(dv1) + "0"
            
            if int(dv) != int(dv_calculado):
                self.errors.append("CNS inválido - dígito verificador incorreto")
                return False
                    
        elif str(cns).startswith(('7', '8', '9')):  # CNS Provisório
            soma = 0
            for i in range(15):
                produto = int(str(cns)[i]) * (15 - i)
                soma += produto
            
            if soma % 11 != 0:
                self.errors.append("CNS inválido - dígito verificador incorreto")
                return False
        else:
            self.errors.append("CNS inválido - deve começar com 1, 2, 7, 8 ou 9")
            return False
                
        return True

    def validate_cnes(self, cnes: str) -> bool:
        """Valida dígito verificador do CNES"""
        if not self._validate_digits(cnes, "CNES", self.REQUIRED_SIZES['cnes']):
            return False

        # Implementação do algoritmo de validação do CNES
        soma = 0
        peso = 2
        for i in range(5, -1, -1):
            soma += int(str(cnes)[i]) * peso
            peso += 1
            if peso > 9:
                peso = 2
                
        dv = 0 if soma % 11 == 0 else 11 - (soma % 11)
        if dv == 10:
            dv = 0
            
        if int(str(cnes)[-1]) != dv:
            self.errors.append("CNES inválido - dígito verificador incorreto")
            return False
            
        return True

    def validate_competencia(self, competencia: str) -> bool:
        """Valida se a competência está no formato YYYYMM e é uma data válida não futura"""
        if not self._validate_digits(competencia, "Competência", self.REQUIRED_SIZES['competencia']):
            return False
            
        try:
            year = int(competencia[:4])
            month = int(competencia[4:])
            if month < 1 or month > 12:
                self.errors.append("Mês da competência deve estar entre 01 e 12")
                return False
                
            today = datetime.now()
            comp_date = datetime(year, month, 1)
            
            if comp_date > today:
                self.errors.append("Competência não pode ser futura")
                return False
                
            return True
        except:
            self.errors.append("Competência inválida")
            return False

    def validate_required_fields(self, data: dict, required_fields: list) -> bool:
        """Valida presença de campos obrigatórios"""
        missing = [f for f in required_fields if not data.get(f)]
        if missing:
            self.errors.extend(f"Campo obrigatório ausente: {f}" for f in missing)
            return False
        return True

    def validate_header(self, header_data: dict) -> bool:
        """Valida os dados do cabeçalho do arquivo BPA"""
        self.errors = []
        
        if not self.validate_required_fields(header_data, self.REQUIRED_HEADER_FIELDS):
            return False
        
        if not self.validate_competencia(header_data['year_month']):
            return False
        
        cgc_cpf = str(header_data['cgc_cpf']).replace('.','').replace('-','').replace('/','')
        if not cgc_cpf.isdigit():
            self.errors.append("CGC/CPF deve conter apenas números")
            return False
        
        if header_data['dest_type'] not in self.VALID_DEST_TYPES:
            self.errors.append("Tipo de destino deve ser M ou E")
            return False
            
        return len(self.errors) == 0

    def validate_bpa_i(self, row: pd.Series) -> bool:
        """Valida uma linha de BPA Individualizado"""
        self.errors = []
        
        if not self.validate_required_fields(row, self.REQUIRED_BPA_I_FIELDS):
            return False
        
        if not self.validate_cns(row['cns_paciente']):
            return False
            
        if not self.validate_cns(row['cns_profissional']):
            return False
            
        if not self.validate_cnes(row['cnes']):
            return False
            
        if not self._validate_date(row['data_atendimento'], "Data de atendimento"):
            return False
            
        if row['sexo'] not in self.VALID_SEX:
            self.errors.append("Sexo deve ser M ou F")
            return False
            
        try:
            idade = int(row['idade'])
            if idade < self.MIN_AGE or idade > self.MAX_AGE:
                self.errors.append(f"Idade deve estar entre {self.MIN_AGE} e {self.MAX_AGE} anos")
                return False
        except ValueError:
            self.errors.append("Idade deve ser um número")
            return False
                
        return len(self.errors) == 0
        
    def validate_bpa_c(self, row: pd.Series) -> bool:
        """Valida uma linha de BPA Consolidado"""
        self.errors = []
        
        if not self.validate_required_fields(row, self.REQUIRED_BPA_C_FIELDS):
            return False
        
        if not self.validate_cnes(row['cnes']):
            return False
            
        if not self.validate_competencia(row['competencia']):
            return False
                
        if not self._validate_digits(row['procedimento'], "Procedimento", self.REQUIRED_SIZES['procedimento']):
            return False
            
        try:
            qtd = int(row['quantidade'])
            if qtd < 0:
                self.errors.append("Quantidade não pode ser negativa")
                return False
        except ValueError:
            self.errors.append("Quantidade deve ser um número")
            return False
                
        return len(self.errors) == 0

    def get_errors(self) -> list:
        """Retorna a lista de erros encontrados na última validação"""
        return self.errors