import io
import pandas as pd
import logging
from app.utils.bpa_generator import BPAGenerator
from app.utils.fetch_data import DataFetcher
from app.utils.data_mapping import DATA_MAPPING

class BPAService:
    def __init__(self):
        self.generator = BPAGenerator()
        self.data_fetcher = DataFetcher(schema="public")
        self.logger = logging.getLogger('bpa_service')
        # Constante para definir o tamanho do lote
        self.BATCH_SIZE = 1000
    
    def _load_data(self, year_month: str) -> pd.DataFrame:
        """Carrega dados do banco de dados"""
        try:
            # Tenta buscar dados reais do banco
            self.logger.info(f"Buscando dados para competência {year_month}")
            data = self.data_fetcher.fetch_data_by_competencia(year_month)
            
            if not data:
                self.logger.warning(f"Nenhum dado encontrado para competência {year_month}. Usando dados de exemplo.")
                # Usa os dados de exemplo se não encontrar dados reais
                raw_data = self.data_fetcher.fetch_all_data(DATA_MAPPING)
                
                # Converte os dados para um DataFrame
                records = []
                for _ in range(10):  # Número de registros de exemplo
                    record = {}
                    for field, value in raw_data.items():
                        field_name = field.replace('prd-', '')
                        
                        # Mapeamento simplificado
                        field_mapping = {
                            'ident': 'tipo',
                            'cnes': 'cnes',
                            'cmp': 'competencia',
                            'cnsmed': 'cns_profissional',
                            'dtaten': 'data_atendimento',
                            'flh': 'folha',
                            'seq': 'sequencial',
                            'pa': 'procedimento',
                            'cnspac': 'cns_paciente',
                            'ibge': 'codigo_municipio',
                            'ldade': 'idade',
                            'qt': 'quantidade',
                            'caten': 'carater_atendimento',
                            'naut': 'numero_autorizacao',
                            'org': 'origem',
                            'nmpac': 'nome_paciente',
                            'dtnasc': 'data_nascimento',
                            'sexo': 'sexo',
                            'cid': 'cid',
                            # Adicione outros campos conforme necessário
                        }
                        
                        if field_name in field_mapping:
                            mapped_name = field_mapping[field_name]
                            if isinstance(value, list) and len(value) > 0:
                                record[mapped_name] = value[0][field_mapping[field_name]] if isinstance(value[0], dict) else value
                            else:
                                record[mapped_name] = value
                    
                    # Garante que a competência corresponde à solicitada
                    record['competencia'] = year_month
                    records.append(record)
                
                return pd.DataFrame(records)
            else:
                return pd.DataFrame(data)
                
        except Exception as e:
            self.logger.error(f"Erro ao carregar dados: {str(e)}", exc_info=True)
            raise ValueError(f"Falha ao carregar dados para competência {year_month}: {str(e)}")

    def generate_bpa_file(self, year_month: str, tipo_relatorio: str) -> io.BytesIO:
        """
        Gera o arquivo BPA completo usando processamento em lotes.
        
        Args:
            year_month (str): Mês e ano selecionado pelo usuário.
            tipo_relatorio (str): Tipo do relatório (ex: 'individualizada', 'consolidado').
        
        Returns:
            io.BytesIO: Buffer contendo o arquivo gerado.
        """
        # Carrega dados do banco
        df = self._load_data(year_month)

        if df.empty:
            raise ValueError(f"Nenhum registro encontrado para competência {year_month}")

        # Metadados para o cabeçalho (idealmente viriam de configuração ou banco de dados)
        # TODO: Buscar estes dados de uma tabela de configuração
        header_data = {
            'year_month': year_month,
            'org_name': 'NOME DA ORGANIZAÇÃO',
            'org_acronym': 'SIGLA',
            'cgc_cpf': '12345678901234',
            'dest_name': 'SECRETARIA MUNICIPAL DE SAÚDE',
            'dest_type': 'M',
            'version': '1.0.0',
            'total_lines': len(df) + 1,  # +1 para contar o cabeçalho
            'total_sheets': (len(df) // self.generator.MAX_LINHAS_POR_FOLHA) + 1
        }

        # Criando o buffer de memória
        memoria = io.BytesIO()
        memoria.write(self.generator.generate_header(header_data).encode("utf-8"))

        # Processamento em lotes para evitar consumo excessivo de memória
        total_rows = len(df)
        self.logger.info(f"Iniciando geração de arquivo BPA com {total_rows} registros")
        
        for start_idx in range(0, total_rows, self.BATCH_SIZE):
            end_idx = min(start_idx + self.BATCH_SIZE, total_rows)
            batch = df.iloc[start_idx:end_idx]
            
            self.logger.info(f"Processando lote de registros {start_idx+1} a {end_idx}")
            for _, row in batch.iterrows():
                if tipo_relatorio.lower() == 'individualizada':
                    memoria.write(self.generator.generate_bpa_i(row).encode("utf-8"))
                elif tipo_relatorio.lower() == 'consolidado':
                    memoria.write(self.generator.generate_bpa_c(row).encode("utf-8"))

        memoria.seek(0)
        self.logger.info(f"Arquivo BPA gerado com sucesso")
        return memoria