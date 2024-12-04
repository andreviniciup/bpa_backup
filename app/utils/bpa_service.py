import io
import pandas as pd
from app.utils.bpa_generator import BPAGenerator

# Classe que contém toda a lógica de negócio relacionada ao BPA
class BPAService:
    def __init__(self):
        # Inicializa o gerador de arquivos BPA que contém as regras de formatação
        self.generator = BPAGenerator()
    
    def _load_header_data(self):
        """Carrega os dados do cabeçalho do arquivo CSV de configuração"""
        df_cabecalho = pd.read_csv("app/data/cabeçalho.csv", dtype=str)
        return df_cabecalho.iloc[0].to_dict()
    
    def _load_records(self, tipo_relatorio: str) -> pd.DataFrame:
        """
        Carrega os registros do tipo apropriado (BPA-I ou BPA-C)
        Args:
            tipo_relatorio: "individualizada" ou "consolidado"
        Returns:
            DataFrame com os registros carregados
        """
        if tipo_relatorio == "individualizada":
            return pd.read_csv("app/data/bpa_individualizado.csv", dtype=str)
        elif tipo_relatorio == "consolidado":
            return pd.read_csv("app/data/bpa_consolidado.csv", dtype=str)
        raise ValueError("Tipo de relatório inválido")

    def generate_bpa_file(self, tipo_relatorio: str) -> io.BytesIO:
        """
        Gera o arquivo BPA completo baseado no tipo de relatório
        Args:
            tipo_relatorio: "individualizada" ou "consolidado"
        Returns:
            Buffer de memória contendo o arquivo gerado
        """
        tipo_relatorio = tipo_relatorio.lower()
        header_data = self._load_header_data()
        df_registros = self._load_records(tipo_relatorio)
        
        # Cria buffer em memória para armazenar o arquivo
        memoria = io.BytesIO()
        # Gera e escreve o cabeçalho
        memoria.write(self.generator.generate_header(header_data).encode('utf-8'))
        
        # Gera e escreve cada linha de registro
        for _, row in df_registros.iterrows():
            if tipo_relatorio == "consolidado":
                memoria.write(self.generator.generate_bpa_c(row).encode('utf-8'))
            else:
                memoria.write(self.generator.generate_bpa_i(row).encode('utf-8'))
                
        memoria.seek(0)
        return memoria