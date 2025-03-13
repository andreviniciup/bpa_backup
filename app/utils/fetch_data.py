from .database import Database
import logging
from typing import Dict, List, Any, Optional, Union

class DataFetcher:
    def __init__(self, schema="public"):
        self.db = Database()
        self.schema = schema
        self._setup_logging()
        
    def _setup_logging(self):
        """Configura o sistema de logs"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename='data_fetcher.log'
        )
        self.logger = logging.getLogger('DataFetcher')
    
    def get_connection(self):
        """Obtém uma conexão com o banco de dados"""
        conn = self.db.get_connection()
        if not conn:
            self.logger.error("Falha ao obter conexão com o banco de dados")
            raise ConnectionError("Erro: Não foi possível conectar ao banco de dados.")
        return conn
    
    def _is_valid_identifier(self, identifier: str) -> bool:
        """Verifica se um identificador é válido para uso em SQL (evita injeção)"""
        # Regra simples: somente letras, números e underscores
        if not identifier:
            return False
        return identifier.isalnum() or all(c.isalnum() or c == '_' for c in identifier)
    
    def fetch_table_data(self, table: str, columns: list, where_clause: Dict = None, limit: int = 1) -> List[Dict]:
        """
        Busca dados de uma tabela específica com condições opcionais.
        
        Args:
            table (str): Nome da tabela
            columns (list): Lista de colunas a serem buscadas
            where_clause (dict, opcional): Dicionário de condições {coluna: valor}
            limit (int, opcional): Limite de registros a retornar
            
        Returns:
            List[Dict]: Lista de registros no formato de dicionários
        """
        if not table or not columns:
            self.logger.error("Nome de tabela ou colunas não fornecidos")
            return []
            
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                # Validação dos nomes de tabela e colunas para evitar SQL injection
                if not self._is_valid_identifier(table) or not all(self._is_valid_identifier(col) for col in columns):
                    self.logger.error(f"Nome de tabela ou coluna inválido: {table}, {columns}")
                    raise ValueError("Nome de tabela ou coluna inválido")
                
                col_string = ", ".join(f"\"{col}\"" for col in columns)
                query = f"SELECT {col_string} FROM \"{self.schema}\".\"{table}\""
                
                params = []
                
                # Adiciona condições WHERE se fornecidas
                if where_clause and isinstance(where_clause, dict):
                    conditions = []
                    for col, value in where_clause.items():
                        if not self._is_valid_identifier(col):
                            self.logger.error(f"Nome de coluna na condição WHERE inválido: {col}")
                            raise ValueError(f"Nome de coluna inválido na condição WHERE: {col}")
                        conditions.append(f"\"{col}\" = %s")
                        params.append(value)
                    
                    if conditions:
                        query += " WHERE " + " AND ".join(conditions)
                
                # Adiciona LIMIT
                query += " LIMIT %s;"
                params.append(limit)
                
                self.logger.debug(f"Executando query: {query} com parâmetros: {params}")
                cur.execute(query, params)
                colnames = [desc[0] for desc in cur.description]
                rows = cur.fetchall()
                return [dict(zip(colnames, row)) for row in rows] if rows else []
        except Exception as e:
            self.logger.error(f"Erro ao buscar dados da tabela '{table}': {e}")
            return []
        finally:
            self.db.release_connection(conn)
    
    def _verify_data(self, field: str, value: Any, check_info: Dict) -> bool:
        """
        Verifica se o valor existe na tabela/coluna especificada
        
        Args:
            field (str): Nome do campo sendo verificado
            value (Any): Valor a ser verificado
            check_info (Dict): Informações de verificação do campo
            
        Returns:
            bool: True se válido, False caso contrário
        """
        if not check_info.get("check"):
            return True
            
        check_table = check_info.get("check_table")
        check_column = check_info.get("check_column")
        
        if not check_table or not check_column:
            return True
            
        if not self._is_valid_identifier(check_table) or not self._is_valid_identifier(check_column):
            self.logger.error(f"Nome de tabela ou coluna de verificação inválido: {check_table}, {check_column}")
            return False
            
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                query = f"SELECT 1 FROM \"{self.schema}\".\"{check_table}\" WHERE \"{check_column}\" = %s LIMIT 1;"
                cur.execute(query, (value,))
                return cur.fetchone() is not None
        except Exception as e:
            self.logger.error(f"Erro ao verificar dado '{field}': {e}")
            return False
        finally:
            self.db.release_connection(conn)
    
    def fetch_related_data(self, table: str, column: str, value: Any, 
                          related_table: str, related_column: str) -> Optional[Any]:
        """
        Busca dados relacionados baseados em uma chave estrangeira
        
        Args:
            table (str): Tabela principal
            column (str): Coluna na tabela principal
            value (Any): Valor a buscar
            related_table (str): Tabela relacionada
            related_column (str): Coluna na tabela relacionada
            
        Returns:
            Any: Valor relacionado ou None se não encontrado
        """
        if not self._is_valid_identifier(table) or \
           not self._is_valid_identifier(column) or \
           not self._is_valid_identifier(related_table) or \
           not self._is_valid_identifier(related_column):
            self.logger.error(f"Nome de tabela ou coluna inválido na busca relacionada")
            return None
            
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                query = f"""
                    SELECT r.\"{related_column}\" 
                    FROM \"{self.schema}\".\"{table}\" t
                    JOIN \"{self.schema}\".\"{related_table}\" r 
                    ON t.\"{column}\" = r.\"{column}\"
                    WHERE t.\"{column}\" = %s
                    LIMIT 1;
                """
                cur.execute(query, (value,))
                result = cur.fetchone()
                return result[0] if result else None
        except Exception as e:
            self.logger.error(f"Erro ao buscar dados relacionados: {e}")
            return None
        finally:
            self.db.release_connection(conn)
            
    def fetch_data_by_competencia(self, competencia: str, limit: int = 100) -> List[Dict]:
        """
        Busca dados específicos para uma competência com segurança aprimorada
        
        Args:
            competencia (str): Competência no formato YYYYMM
            limit (int, opcional): Limite de registros
            
        Returns:
            List[Dict]: Lista de registros no formato de dicionários
        """
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                # Validação de entrada
                if not competencia.isdigit() or len(competencia) != 6:
                    self.logger.error(f"Formato de competência inválido: {competencia}")
                    raise ValueError("Formato de competência inválido. Use YYYYMM.")
                
                query = f"""
                    SELECT * FROM \"{self.schema}\".procedimentos 
                    WHERE competencia = %s
                    LIMIT %s;
                """
                cur.execute(query, (competencia, limit))
                colnames = [desc[0] for desc in cur.description]
                rows = cur.fetchall()
                return [dict(zip(colnames, row)) for row in rows] if rows else []
        except Exception as e:
            self.logger.error(f"Erro ao buscar dados para competência '{competencia}': {e}")
            return []
        finally:
            self.db.release_connection(conn)

    def fetch_all_data(self, data_mapping: Dict, fields_to_fetch: List[str] = None, limit: int = 1) -> Dict:
        """
        Busca todos os dados conforme o mapeamento fornecido
        
        Args:
            data_mapping (Dict): Mapeamento de campos com suas informações
            fields_to_fetch (List[str], opcional): Lista de campos específicos a buscar
            limit (int, opcional): Limite de registros por tabela
            
        Returns:
            Dict: Dicionário com os dados buscados
        """
        results = {}
        
        # Se nenhum campo específico for solicitado, busca todos
        fields_to_process = fields_to_fetch if fields_to_fetch else data_mapping.keys()
        
        # Agrupa campos por tabela para fazer menos consultas
        table_groups = {}
        for field in fields_to_process:
            if field not in data_mapping:
                self.logger.warning(f"Campo solicitado '{field}' não encontrado no mapeamento")
                continue
                
            info = data_mapping[field]
            table = info.get("table")
            
            if table == "padrao":
                results[field] = info.get("predefinido", "VALOR PADRÃO NÃO DEFINIDO")
                continue
                
            if table not in table_groups:
                table_groups[table] = {"fields": [], "info": []}
                
            table_groups[table]["fields"].append(field)
            table_groups[table]["info"].append(info)
            
        # Para cada tabela, busca todos os campos de uma vez
        for table, group_data in table_groups.items():
            fields = group_data["fields"]
            info_list = group_data["info"]
            
            # Obtém todas as colunas únicas para esta tabela
            columns = list(set(info["column"] for info in info_list if "column" in info))
            
            if not columns:
                continue
                
            # Busca os dados da tabela
            table_data = self.fetch_table_data(table, columns, limit=limit)
            
            # Se não houver dados, use valores predefinidos
            if not table_data:
                for i, field in enumerate(fields):
                    info = info_list[i]
                    results[field] = info.get("predefinido", "VALOR PADRÃO NÃO DEFINIDO")
                continue
                
            # Processa cada campo
            for i, field in enumerate(fields):
                info = info_list[i]
                column = info.get("column")
                
                # Se não houver coluna especificada, pula
                if not column:
                    continue
                    
                # extrai o valor do primeiro resultado
                value = table_data[0].get(column) if table_data else None
                
                # verifica a integridade se necessário
                if info.get("check") and value is not None:
                    is_valid = self._verify_data(field, value, info)
                    if not is_valid:
                        self.logger.warning(f"Verificação falhou para o campo '{field}' com valor '{value}'")
                        value = info.get("predefinido", None)
                        
                results[field] = value if value is not None else info.get("predefinido", "VALOR PADRÃO NÃO DEFINIDO")
                
        return results

    def fetch_custom_data(self, data_mapping: Dict, custom_conditions: Dict[str, Dict], 
                          fields_to_fetch: List[str] = None, limit: int = 1) -> Dict:
        """
        busca dados com condições personalizadas
        
        args:
            data_mapping (Dict): Mapeamento de campos com suas informaçoes
            custom_conditions (Dict[str, Dict]): Condições por tabela {tabela: {coluna: valor}}
            fields_to_fetch (List[str], opcional): Lista de campos específicos a buscar
            limit (int, opcional): Limite de registros por tabela
            
        returns:
            dict: Dicionario com os dados buscados
        """
        results = {}
        
        # se nenhum campo especifico for solicitado, busca todos
        fields_to_process = fields_to_fetch if fields_to_fetch else data_mapping.keys()
        
        # agrupa campos por tabela para fazer menos consultas
        table_groups = {}
        for field in fields_to_process:
            if field not in data_mapping:
                self.logger.warning(f"Campo solicitado '{field}' não encontrado no mapeamento")
                continue
                
            info = data_mapping[field]
            table = info.get("table")
            
            if table == "padrao":
                results[field] = info.get("predefinido", "VALOR PADRÃO NÃO DEFINIDO")
                continue
                
            if table not in table_groups:
                table_groups[table] = {"fields": [], "info": []}
                
            table_groups[table]["fields"].append(field)
            table_groups[table]["info"].append(info)
            
        # para cada tabela, busca todos os campos de uma vez com as condiçoes especificas
        for table, group_data in table_groups.items():
            fields = group_data["fields"]
            info_list = group_data["info"]
            
            # obtém todas as colunas unicas para esta tabela
            columns = list(set(info["column"] for info in info_list if "column" in info))
            
            if not columns:
                continue
                
            # obtem condições para esta tabela, se existirem
            where_clause = custom_conditions.get(table, {})
            
            # busca os dados da tabela com as condiçoes especificadas
            table_data = self.fetch_table_data(table, columns, where_clause=where_clause, limit=limit)
            
            # se nao houver dados, use valores predefinidos
            if not table_data:
                for i, field in enumerate(fields):
                    info = info_list[i]
                    results[field] = info.get("predefinido", "VALOR PADRÃO NÃO DEFINIDO")
                continue
                
            # processa cada campo
            for i, field in enumerate(fields):
                info = info_list[i]
                column = info.get("column")
                
                # se nao houver coluna especificada, pula
                if not column:
                    continue
                    
                # extrai o valor do primeiro resultado
                value = table_data[0].get(column) if table_data else None
                
                # verifica a integridade se necessario
                if info.get("check") and value is not None:
                    is_valid = self._verify_data(field, value, info)
                    if not is_valid:
                        self.logger.warning(f"Verificação falhou para o campo '{field}' com valor '{value}'")
                        value = info.get("predefinido", None)
                        
                results[field] = value if value is not None else info.get("predefinido", "VALOR PADRÃO NÃO DEFINIDO")
                
        return results