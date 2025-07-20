import json
import subprocess
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
        funcao = 'context'
        command = ['node', self.scraper_script_path, funcao, text, source_lang, target_lang]
        print(f"🐍 Python: Executando comando -> {' '.join(command)}")
        return run_cmd(command)  # <- Faltava o return aqui!

    def get_translation(self, text: str, transSource: str, transTarget: str) -> Optional[Dict]:
        funcao = 'translation'
        command = ['node', self.scraper_script_path, funcao, text, transSource, transTarget]
        print(f"🐍 Python: Executando comando -> {' '.join(command)}")
        return run_cmd(command)

if __name__ == "__main__":
    scraper = ReversoScraperService()
    print("--- Início do teste ---")

    data = scraper.get_context("nice", "english", "portuguese")
    
    if data and 'examples' in data:
        print(f"\n✅ Dados recebidos. Primeiro exemplo: {data['examples'][0]['source']}")
    else:
        print("\n⚠️ Dados recebidos, mas parecem estar vazios ou em formato inesperado.")

    if data:
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))
        os.makedirs(output_dir, exist_ok=True)  # Garante que 'data/' exista

        output_filename = os.path.join(output_dir, "output.json")

        print(f"\nTentando escrever em '{output_filename}'...")

        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"🎉 Arquivo salvo com sucesso em: {output_filename}")
        except IOError as e:
            print(f"❌ ERRO CRÍTICO: Falha ao salvar arquivo.")
            print(f"   Detalhes: {e}")

    print('\n--- Fim do teste ---')
