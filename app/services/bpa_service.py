import io
import pandas as pd
from app.utils.bpa_generator import BPAGenerator

class BPAService:
    def __init__(self):
        self.generator = BPAGenerator()
    
    def _load_data(self) -> pd.DataFrame:
        """Carrega todos os dados do 'banco de dados' (CSV)"""
        return pd.read_csv("app/data/database.csv", dtype=str)

    def generate_bpa_file(self, year_month: str, tipo_relatorio: str) -> io.BytesIO:
        """
        Gera o arquivo BPA completo.
        
        Args:
            year_month (str): Mês e ano selecionado pelo usuário.
            tipo_relatorio (str): Tipo do relatório (ex: 'individualizada', 'consolidado').
        
        Returns:
            io.BytesIO: Buffer contendo o arquivo gerado.
        """
        df = self._load_data()

        # Filtra pelo 'year_month' selecionado pelo usuário
        df_filtered = df[df["competencia"] == year_month]

        if df_filtered.empty:
            raise ValueError(f"Nenhum registro encontrado para competência {year_month}")

        header_data = df_filtered.iloc[0].to_dict()

        # Criando o buffer de memória
        memoria = io.BytesIO()
        memoria.write(self.generator.generate_header(header_data).encode("utf-8"))

        for _, row in df_filtered.iterrows():
            memoria.write(self.generator.generate_bpa_i(row).encode("utf-8"))

        memoria.seek(0)
        return memoria
