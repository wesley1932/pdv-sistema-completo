import json
import os
from datetime import datetime

class ConfigManager:
    def __init__(self, config_file='config/config.json'):
        self.config_file = config_file
        self.default_config = {
            'theme': {
                'primary_color': '#2c3e50',
                'secondary_color': '#3498db',
                'background_color': '#ecf0f1',
                'text_color': '#2c3e50',
                'button_color': '#3498db',
                'button_text_color': '#ffffff'
            },
            'company': {
                'name': 'Sistema PDV',
                'logo_path': 'assets/logo.png',
                'address': '',
                'phone': '',
                'email': ''
            },
            'system': {
                'auto_backup': True,
                'backup_interval_hours': 24,
                'low_stock_alert': True,
                'currency_symbol': 'R$',
                'decimal_places': 2
            },
            'printer': {
                'enabled': False,
                'printer_name': '',
                'paper_size': 'A4'
            }
        }
        self.config = self.load_config()
    
    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Mesclar com configuração padrão para garantir todas as chaves
                    return self.merge_configs(self.default_config, loaded_config)
            else:
                self.save_config(self.default_config)
                return self.default_config.copy()
        except Exception as e:
            print(f"Erro ao carregar configuração: {e}")
            return self.default_config.copy()
    
    def merge_configs(self, default, loaded):
        """Mescla configurações, mantendo estrutura padrão"""
        result = default.copy()
        for key, value in loaded.items():
            if key in result and isinstance(value, dict) and isinstance(result[key], dict):
                result[key].update(value)
            else:
                result[key] = value
        return result
    
    def save_config(self, config=None):
        if config is None:
            config = self.config
        
        try:
            # Criar diretório se não existir
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar configuração: {e}")
            return False
    
    def get(self, key_path, default=None):
        """Obter valor por caminho (ex: 'theme.primary_color')"""
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path, value):
        """Definir valor por caminho"""
        keys = key_path.split('.')
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
        self.save_config()
    
    def get_theme(self):
        return self.config.get('theme', self.default_config['theme'])
    
    def get_company_info(self):
        return self.config.get('company', self.default_config['company'])
    
    def get_system_settings(self):
        return self.config.get('system', self.default_config['system'])
    
    def update_theme(self, theme_data):
        self.config['theme'].update(theme_data)
        self.save_config()
    
    def update_company_info(self, company_data):
        self.config['company'].update(company_data)
        self.save_config()
    
    def reset_to_default(self):
        self.config = self.default_config.copy()
        self.save_config()