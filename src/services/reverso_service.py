# src/services/reverso_service.py
import os
from typing import Dict, Optional
from utils.run_cmd import run_cmd

class ReversoScraperService:
    def __init__(self):
        current_dir = os.path.dirname(__file__)
        project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
        self.scraper_script_path = os.path.join(project_root, 'reverso_scraper', 'get_data.js')
        if not os.path.isfile(self.scraper_script_path):
            raise FileNotFoundError(f"Script do scraper não encontrado em: {self.scraper_script_path}")
        
    def get_context(self, text: str, source_lang: str, target_lang: str) -> Optional[Dict]:
        command = ['node', self.scraper_script_path, 'context', text, source_lang, target_lang]
        print(f"Executando comando: {' '.join(command)}")
        return run_cmd(command)
