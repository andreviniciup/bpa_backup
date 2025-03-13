import json
import os
import logging
from typing import Dict, Any

class ConfigReader:
    """Classe para gerenciar configurações do sistema BPA"""
    
    def __init__(self, config_path="config"):
        self.config_path = config_path
        self.logger = logging.getLogger('config_reader')
        self.config_cache = {}
    
    def get_config(self, config_name: str) -> Dict[str, Any]:
        """
        Carrega uma configuração específica do arquivo JSON.
        
        Args:
            config_name: Nome do arquivo de configuração (sem a extensão .json)
            
        Returns:
            Dicionário com as configurações
        """
        if config_name in self.config_cache:
            return self.config_cache[config_name]
            
        file_path = os.path.join(self.config_path, f"{config_name}.json")
        
        try:
            if not os.path.exists(file_path):
                self.logger.warning(f"Arquivo de configuração não encontrado: {file_path}")
                return {}
                
            with open(file_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.config_cache[config_name] = config
                return config
        except Exception as e:
            self.logger.error(f"Erro ao carregar configuração {config_name}: {str(e)}")
            return {}
    
    def get_org_config(self) -> Dict[str, Any]:
        """Retorna a configuração da organização"""
        return self.get_config('organization')
    
    def get_data_mapping(self) -> Dict[str, Any]:
        """Retorna o mapeamento de dados para BPA"""
        return self.get_config('data_mapping')
    
    def reload_config(self, config_name: str = None):
        """
        Recarrega as configurações do cache
        
        Args:
            config_name: Nome específico da configuração ou None para recarregar todas
        """
        if config_name:
            if config_name in self.config_cache:
                del self.config_cache[config_name]
        else:
            self.config_cache.clear()